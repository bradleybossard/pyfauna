class LindenmayerParse(object):
  def __init__(self, iterations, axiom, rules):
    self.iterations = iterations
    self.axiom = axiom
    self.rules = rules

  def iterate(self):
    if self.axiom == None or not self.rules:
      return
    result = self.axiom
    for repeat in range(0, self.iterations):
      result = self.translate(result)
    return result

  def translate(self, axiom):
    result = []
    for i in axiom:
      if i in self.rules:
        result += self.rules[i]
      else:
        result += i

    return result
