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
    root.set("transform", "translate(%f, %f)" % (-minX, -minY))
    root.set("class", "aqua")
    root.set("d", path)
    for element in animationElements:
        root.append(element)
    return root

  # TODO(bradleybossard) : Might need to calculate the path length here as well.
  def calcBoundingBox(self, stack):
    cur_x = cur_y = 0
    x = []
    y = []
    for point in stack:
      if point['command'] == 'M':
        x.append(point['x'])
        y.append(point['y'])
      elif point['command'] == 'l':
        cur_x += point['x']
        cur_y += point['y']
        x.append(cur_x)
        y.append(cur_y)
    return (min(x), min(y), max(x), max(y))

  def renderPathData(self, pointStack):
    pathData = []
    for point in pointStack:
      pathData.append("%s %f %f\n" % (point['command'], point['x'], point['y']))
    return ''.join(pathData)

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
