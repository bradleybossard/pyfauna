from lxml import etree

class SvgWriter():
  def __init__(self, paths):
    self.paths = paths

  # TODO(bradleybossard) : Rename to render, move name to initialization.
  def toSvg(self, name):
    xValues = []
    yValues = []
    for path in self.paths:
      xValues.append(path['bbox'][0])
      yValues.append(path['bbox'][1])
      xValues.append(path['bbox'][2])
      yValues.append(path['bbox'][3])

    minX = min(xValues)
    maxX = max(xValues)
    minY = min(yValues)
    maxY = max(yValues)

    svgWidth = str(abs(maxX - minX))
    svgHeight = str(abs(maxY - minY))

    xlink_url = "http://www.w3.org/1999/xlink"

    NSMAP = {"dc" : "http://purl.org/dc/elements/1.1",
             "xlink" : xlink_url,
             "dc": "http://purl.org/dc/elements/1.1/",
             "cc": "http://creativecommons.org/ns#",
             "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
             None: "http://www.w3.org/2000/svg",
             "svg": "http://www.w3.org/2000/svg"}

    root = etree.Element("svg", nsmap=NSMAP)
    root.set("viewBox", "0 0 " + svgWidth + " " + svgHeight)
    root.set("width", svgWidth)
    root.set("height", svgHeight)

    instance = etree.Element("use")
    instance.set("x", "0")
    instance.set("y", "0")
    instance.set("stroke", "black")
    instance.set("stroke-width", "1")
    instance.set("fill", "none")
    instance.set("{%s}href" % xlink_url, "#" + name)

    root.append(instance)
    defs = etree.Element("defs")
    defs.append(self.paths[0]["path"])
    root.append(defs)

    return etree.tostring(root)
