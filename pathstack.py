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

        ang = ((angle % 360) / 180) * 3.141596;
        #deltaX = round(lineLength * math.cos(math.radians(angle)), self.precision)
        deltaX = round(lineLength * math.cos(ang), self.precision)
        #deltaY = round(lineLength * math.sin(math.radians(angle)), self.precision)
        deltaY = round(lineLength * math.sin(ang), self.precision)
        pointStack.append(self.createCommand('l', deltaX, deltaY))
        point = (round(point[0] + deltaX, self.precision), round(point[1] + deltaY, self.precision))

        jsangle = ((angle % 360) / 180) * 3.141596;
        #print(angle, jsangle)

        #var ang = ((angle % 360) / 180) * Math.PI;
        #currentPoint.x += Math.cos(ang) * length;
        #currentPoint.y += Math.sin(ang) * length;
        #pointStack.push( {'command': 'L',
	#		'point': {'x': currentPoint.x, 'y': currentPoint.y },
	#		'depth': pointStack.length } );

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

