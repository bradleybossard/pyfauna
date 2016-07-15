from operator import itemgetter
from lxml import etree
from math import sqrt
import random

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

  def calcPathLength(self, stack):
    length = 0.0
    for point in stack:
      if point['command'] == 'l':
        x = point['x']
        y = point['y']
        length += sqrt((x * x) + (y * y))
    return length

  def renderPathData(self, pointStack):
    pathData = []
    for point in pointStack:
      pathData.append("%s %f %f\n" % (point['command'], point['x'], point['y']))
    return ''.join(pathData)

  def shufflePath(self, pointStack):
      head = None
      tail = []
      final = []
      for point in pointStack:
          if point['command'] == 'M':
              if head != None:
                  final.append(head)
                  random.shuffle(tail)
                  final.extend(tail)
                  tail = []
              head = point
          else:
              tail.append(point)

      final.append(head)
      random.shuffle(tail)
      final.extend(tail)
      return final

  def render(self):
    animationElements = []
    fromPath = self.renderPathData(self.pointStacks[0])
    boundingBox = self.calcBoundingBox(self.pointStacks[0])
    pathLength = self.calcPathLength(self.pointStacks[0])
    #random.shuffle(self.pointStacks[1])
    #toPath = self.renderPathData(self.pointStacks[1])
    toPath = self.renderPathData(self.shufflePath(self.pointStacks[1]))
    #shuffled = self.shufflePath(self.pointStacks[1])
    #toPath = self.renderPathData(shuffled)
    valuesPath = fromPath + ';' +  toPath + ';' + fromPath + ';'
    animationElements.append(self.createPathAnimationElement(fromPath, fromPath, valuesPath))

    boundingBox = self.calcBoundingBox(self.pointStacks[0])

    pathSvg = self.createPathElement(fromPath, boundingBox[0], boundingBox[1], animationElements)

    return {'path': pathSvg, 'bbox': boundingBox}
