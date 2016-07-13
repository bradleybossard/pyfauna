from operator import itemgetter
from lxml import etree

class SvgPathWriter():
  def __init__(self, name, pointStacks):
    self.name = name
    self.pointStacks = pointStacks

  def createPathAnimationElement(self, toPath, fromPath, valuesPath):
    root = etree.Element("animate")
    root.set("attributeName", "d")
    root.set("begin", "0s")
    root.set("dur", "10s")
    root.set("from", fromPath)
    root.set("to", toPath)
    root.set("values", valuesPath)
    root.set("repeatCount", "indefinite")
    return root

  def createStrokeAnimationElement(self, pathLength):
    root = etree.Element("animate")
    root.set("id", "dashanim1")
    root.set("attributeName", "stroke-dashoffset")
    root.set("begin", "0s")
    root.set("dur", "10s")
    #root.set("from", str(pathLength))
    root.set("from", "200.0")
    root.set("to", "0")
    root.set("fill", "freeze")
    root.set("keysplines", "0 0.5 0.5 1")
    root.set("calcmode", "spline")
    root.set("repeatCount", "indefinite")
    return root

  def createPathElement(self, path, minX, minY, animationElements):
    root = etree.Element("path")
    root.set("id", self.name)
    root.set("transform", "translate(" + str(minX * -1) + "," +  str(minY * -1) + ")")
    root.set("class", "aqua")
    root.set("d", path)
    for element in animationElements:
        root.append(element)
    return root

  # TODO(bradleybossard) : Might need to calculate the path length here as well.
  def calcBoundingBox(self, stack):
    currentPoint = (0, 0)
    points = []
    for point in stack:
      if point['command'] == 'M':
        currentPoint = point['point']
        points.append(currentPoint)
      elif point['command'] == 'l':
        currentPoint = (currentPoint[0] + point['point'][0], currentPoint[1] + point['point'][1])
        points.append(currentPoint)

    xValues = map(itemgetter(0), points)
    yValues = map(itemgetter(1), points)
    minX = min(xValues)
    maxX = max(xValues)
    minY = min(yValues)
    maxY = max(yValues)
    return (minX, minY, maxX, maxY)

  def renderPathData(self, pointStack):
    pathData = ''
    for point in pointStack:
      pathData += point['command'] + ' ' + str(point['point'][0]) + ' ' + str(point['point'][1]) + '\n'
    return pathData

  def render(self):
    animationElements = []
    fromPath = self.renderPathData(self.pointStacks[0])
    if(True):
      pathLength = 1.0
      toPath = self.renderPathData(self.pointStacks[1])
      valuesPath = fromPath + ';' +  toPath + ';' + fromPath + ';'
      animationElements.append(self.createPathAnimationElement(fromPath, fromPath, valuesPath))
      animationElements.append(self.createStrokeAnimationElement(pathLength))

    boundingBox = self.calcBoundingBox(self.pointStacks[0])

    pathSvg = self.createPathElement(fromPath, boundingBox[0], boundingBox[1], animationElements)

    return {'path': pathSvg, 'bbox': boundingBox}
