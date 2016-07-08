import re

class lsystem(object):
  def __init__(self, iterations, axiom, rules):
    self.iterations = iterations
    self.axiom = axiom
    self.rules = rules

  def rule(self, match):
    match = match.group()
    if match in self.rules:
        return self.rules[match]
    else:
        return match

  def iterate(self):
      iterated = self.axiom
      for i in range(self.iterations):
          iterated = re.sub(r'\w', self.rule, iterated)
      return iterated
