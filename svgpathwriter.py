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
    #return etree.tostring(root)
    return root

  def createStrokeAnimationElement(self, pathLength):
    output = '<animate id="dashanim1" \n \
             attributeName="stroke-dashoffset" \n \
             from="' + str(pathLength) + '" to="0" dur="10s" begin="0s" \n \
             repeatCount="indefinite" \
             fill="freeze"\n \
             keysplines="0 0.5 0.5 1" \
             calcmode="spline"/>\n'
    return output

  def createPathElement(self, path, minX, minY, animationElements):
    root = etree.Element("path")
    root.set("id", self.name)
    root.set("transform", "translate(" + str(minX * -1) + "," +  str(minY * -1) + ")")
    root.set("class", "")
    root.set("d", path)
    for element in animationElements:
        root.append(element)
    return etree.tostring(root)

  """
  def createStyleElement(self, styleStream, pathLength):
    # TODO(bradleybossard): Encapsulate this into a function
    animateStroke = True
    output = ''
    #strokeLength = str(pathLength * 0.001)
    strokeLength = str(pathLength)
    animateStyle = '  stroke-dasharray: ' + strokeLength + ' ' + strokeLength + ';\n'
    animateStyle += '  stroke-dashoffset: 0;\n'
    #output = '<style>.aqua{' + styleStream + animateStyle + '}</style>'
    return output
  """

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
    if(len(self.pointStacks) > 1):
      toPath = self.renderPathData(self.pointStacks[1])
      valuesPath = fromPath + ';' +  toPath + ';' + fromPath + ';'
      animationElements.append(self.createPathAnimationElement(fromPath, fromPath, valuesPath))

    boundingBox = self.calcBoundingBox(self.pointStacks[0])

    pathSvg = self.createPathElement(fromPath, boundingBox[0], boundingBox[1], animationElements)

    return {'path': pathSvg, 'bbox': boundingBox}
