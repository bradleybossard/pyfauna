import math

class PathStack():
  def __init__(self, alpha, length, lengthGrowth, angleGrowth, stream):
    self.lineLength = length
    self.alpha = alpha
    self.lengthGrowth = lengthGrowth
    self.angleGrowth = angleGrowth

    self.stream = stream
    self.point = (0, 0)
    self.angle = -90
    self.pathLength = 0;
    self.stack = []
    self.pointStack = []

  def createCommand(self, command, x, y):
    return {'command': command, 'point': (x, y)}

  def toPaths(self):
    # Initial position of path
    self.pointStack.append(self.createCommand('M', 0, 0))

    for c in self.stream:
      if c == '<':
        self.alpha -= self.angleGrowth
      elif c == '>':
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
        self.pointStack.append(self.createCommand('l', deltaX, deltaY))
        self.point = (self.point[0] + deltaX, self.point[1] + deltaY)
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
        self.pointStack.append(self.createCommand('M', self.point.x, self.point.y))
      elif c == '!':
        self.angle *= -1
      elif c == '|':
        self.angle += 180

    return self.pointStack

