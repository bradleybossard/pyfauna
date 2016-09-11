from operator import itemgetter
from lxml import etree
from math import sqrt
import random

class SvgPathWriter():
    def __init__(self, name, pointStacks, config):
        self.name = name
        self.pointStacks = pointStacks
        self.config = config
        self.min_x = float("inf")
        self.max_x = float("-inf")
        self.min_y = float("inf")
        self.max_y = float("-inf")

    def createPathAnimationElement(self, toPath, fromPath, valuesPath, config):
        root = etree.Element("animate")
        root.set("attributeName", "d")
        root.set("begin", "0s")
        #root.set("dur", "10s")
        root.set("dur", config['animation_duration'])
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

    def calcBoundingBoxStack(self, stack):
        for point in stack:
            if point['command'] == 'M':
                cur_x = point['x']
                cur_y = point['y']
            elif point['command'] == 'l':
                cur_x += point['x']
                cur_y += point['y']
            self.min_x = round(min(cur_x, self.min_x), 5)
            self.max_x = round(max(cur_x, self.max_x), 5)
            self.min_y = round(min(cur_y, self.min_y), 5)
            self.max_y = round(max(cur_y, self.max_y), 5)


    def calcBoundingBox(self, use_all):
        cur_x = cur_y = 0
        if use_all:
            for stack in self.pointStacks:
                self.calcBoundingBoxStack(stack)
        else:
            self.calcBoundingBoxStack(self.pointStacks[0])


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
            pathData.append("%s %f %f " % (point['command'], point['x'], point['y']))
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
        self.calcBoundingBox(True)
        boundingBox = (self.min_x, self.min_y, self.max_x, self.max_y)
        pathLength = self.calcPathLength(self.pointStacks[0])
        if len(self.pointStacks) > 1:
            toPath = self.renderPathData(self.pointStacks[1])
            #toPath = self.renderPathData(self.shufflePath(self.pointStacks[1]))
            valuesPath = fromPath + ';' +  toPath + ';' + fromPath + ';'
            animationElements.append(self.createPathAnimationElement(fromPath, fromPath, valuesPath, self.config))

        pathSvg = self.createPathElement(fromPath, boundingBox[0], boundingBox[1], animationElements)

        return {'path': pathSvg, 'bbox': boundingBox, 'length': pathLength}
