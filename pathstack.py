import math

class PathStack():
  def __init__(self):
    self.precision = 5

  def createCommand(self, command, x, y):
    return {'command': command, 'x': x, 'y': y}

  def toPaths(self, alpha, length, lengthGrowth, angleGrowth, stream):
    point = (0, 0)
    angle = -90
    pathLength = 0;
    lineLength = length
    stack = []
    pointStack = []

    # Initial position of path
    pointStack.append(self.createCommand('M', 0, 0))

    for c in stream:
      if c == '<':
        alpha -= angleGrowth
      elif c == '>':
        alpha += angleGrowth
      elif c == '(':
        lineLength -= lengthGrowth
      elif c == ')':
        lineLength += lengthGrowth
      elif c == 'F':
        # Move forward
        deltaX = round(lineLength * math.cos(math.radians(angle)), self.precision)
        deltaY = round(lineLength * math.sin(math.radians(angle)), self.precision)
        pointStack.append(self.createCommand('l', deltaX, deltaY))
        point = (round(point[0] + deltaX, self.precision), round(point[1] + deltaY, self.precision))
      elif c == '+':
        # rotate clockwise
        angle += alpha;
      elif c == '-':
        # rotate anti-clockwise
        angle -= alpha;
      elif c == '[':
        # Push the current turtle state to the stack
        stack.append((angle, point))
      elif c == ']':
        # restore the transform and orientation from the stack
        angle, point = stack.pop()
        pointStack.append(self.createCommand('M', point[0], point[1]))
      elif c == '!':
        angle *= -1
      elif c == '|':
        angle += 180

    return pointStack

