#!/usr/bin/python
import math
from operator import itemgetter

class PathStack():
  def __init__(self, alpha, length, lengthGrowth, angleGrowth, stream):
    self.lineLength = length
    self.alpha = alpha
    self.lengthGrowth = lengthGrowth
    self.angleGrowth = angleGrowth

    self.stream = stream
    self.point = (0, 0)
    self.pathLength = 0;
    self.stack = []
    self.pointStack = []

  def toPaths(self):
    paths = []

    # Point north
    self.angle = -90
    point = (0,0)

    # Initial position of path
    self.pointStack.append({'command': 'M', 'point': (0, 0)})

    # TODO(bradleybossard) : Get rid of stream terminology
    for i in range(len(self.stream)):
      c = self.stream[i]

      if c == '<':
        #self.angle -= self.angleGrowth
        self.alpha -= self.angleGrowth
      elif c == '>':
        #self.angle += self.angleGrowth
        self.alpha += self.angleGrowth
      elif c == '(':
        self.lineLength -= self.lengthGrowth
      elif c == ')':
        self.lineLength += self.lengthGrowth
      elif c == 'F':
        # Move forward
        deltaX = self.lineLength * math.cos(math.radians(self.angle))
        deltaX = deltaX if abs(deltaX) > 0.000001 else 0
        deltaY = self.lineLength * math.sin(math.radians(self.angle))
        deltaY = deltaY if abs(deltaY) > 0.000001 else 0
        self.pointStack.append({'command': 'l', 'point':(deltaX, deltaY)})
        #print self.lineLength, self.angle, deltaX, deltaY
        self.point = (self.point[0] + deltaX, self.point[1] + deltaY)
        # TODO(bradleybossard) : t does a curving paths, need to explore more.
      elif c == '+':
        # rotate clockwise
        self.angle += self.alpha;
      elif c == '-':
        # rotate anti-clockwise
        self.angle -= self.alpha;
      elif c == '[':
        # Push the current turtle state to the stack
        self.stack.append((self.angle, self.point))
      elif c == ']':
        # restore the transform and orientation from the stack
        self.angle, self.point = self.stack.pop()
        self.pointStack.append({'command': 'M', 'point': self.point})
      elif c == '!':
        self.angle *= -1
      elif c == '|':
        self.angle += 180
      #print c, self.point

    return self.pointStack

