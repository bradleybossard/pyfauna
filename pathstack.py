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
      if c == '(':
        #alpha -= angleGrowth
        alpha *= 1 - angleGrowth
      elif c == ')':
        #alpha += angleGrowth
        alpha *= 1 + angleGrowth
      elif c == '<':
        lineLength *= 1 - lengthGrowth
      elif c == '>':
        lineLength *= 1 + lengthGrowth
      elif c == 'F':
        # Move forward

	# Revisit this once all l-systems have been added.  The three commented lines
	# lines below represent how this calculation was made in the original working
        # js demo, but causing a shearing effect with Hilbert.
        deltaX = round(lineLength * math.cos(math.radians(angle)), self.precision)
        deltaY = round(lineLength * math.sin(math.radians(angle)), self.precision)
        #ang = ((angle % 360) / 180) * 3.141596;
        #deltaX = round(lineLength * math.cos(ang), self.precision)
        #deltaY = round(lineLength * math.sin(ang), self.precision)

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
        stack.append((angle, point, alpha))
      elif c == ']':
        # restore the transform and orientation from the stack
        angle, point, alpha = stack.pop()
        pointStack.append(self.createCommand('M', point[0], point[1]))
      elif c == '!':
        angle *= -1
      elif c == '|':
        angle += 180

    return pointStack

