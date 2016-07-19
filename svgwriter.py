from lxml import etree

class SvgWriter():
  def __init__(self, paths):
    self.paths = paths

  def createStyleElement(self, classname, stroke_dash_length):
    fill = '#996300'
    fill_opacity = '0.2'
    stroke = '#FFA500'
    stroke_width = '1px'
    stroke_dash = '200.0'
    stroke_linecap = 'butt'
    stroke_linejoin = 'miter'
    stroke_width = '1px'
    stroke_opacity = '0.8'
    stroke_dash_offset = '0.0'
    style = etree.Element("style")
    attributes = [];
    #attributes.append("fill: %s;" % fill)
    attributes.append("fill-opacity: %s;" % fill_opacity)
    attributes.append("stroke: %s;" % stroke)
    attributes.append("stroke-linecap: %s;" % stroke_linecap)
    attributes.append("stroke-linejoin: %s;" % stroke_linejoin)
    attributes.append("stroke-width: %s;" % stroke_width)
    attributes.append("stroke-opacity : %s;" % stroke_opacity)
    dash_length = stroke_dash_length / 2
    attributes.append("stroke-dasharray: %f %f;" % (dash_length, dash_length))
    #attributes.append("stroke-dasharray: 1000 12000 2000 100 1000;")
    #attributes.append("stroke-dasharray: 50%;")
    #attributes.append("stroke-dasharray: 100;")
    attributes.append("stroke-dashoffset: %s;" % stroke_dash_offset)
    #attributes.append("transition: stroke-dashoffset 8s linear;")
    attributes.append("animation: draw 15s alternate infinite;")
    attributes.append("animation: color 5s alternate infinite;")

    # TODO: Add classname
    class_def = ".%s { %s }" % (classname, ''.join(attributes))
    class_def += " @keyframes draw { from { stroke-dashoffset: %s; } to { stroke-dashoffset: 0; } }" % stroke_dash_length
    class_def += " @keyframes color { from { fill: %s; } to { fill: %s; } }" % ('#FF0000', '#00FF00')
    style.text = class_def
    return style


  # TODO(bradleybossard) : Rename to render, move name to initialization.
  def toSvg(self, name):
    xValues = []
    yValues = []
    for path in self.paths:
      print path['length']
      print path['bbox']
      xValues.append(path['bbox'][0])
      yValues.append(path['bbox'][1])
      xValues.append(path['bbox'][2])
      yValues.append(path['bbox'][3])

    minX = min(xValues)
    maxX = max(xValues)
    minY = min(yValues)
    maxY = max(yValues)

    svgWidth = abs(maxX - minX)
    svgHeight = abs(maxY - minY)

    xlink_url = "http://www.w3.org/1999/xlink"

    NSMAP = {"dc" : "http://purl.org/dc/elements/1.1",
             "xlink" : xlink_url,
             "dc": "http://purl.org/dc/elements/1.1/",
             "cc": "http://creativecommons.org/ns#",
             "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
             None: "http://www.w3.org/2000/svg",
             "svg": "http://www.w3.org/2000/svg"}

    root = etree.Element("svg", nsmap=NSMAP)
    root.set("viewBox", "%f %f %f %f" % (0, 0, svgWidth, svgHeight))
    #root.set("viewBox", "%f %f %f %f" % (minX, minY, maxX, maxY))
    #root.set("viewBox", "%f %f %f %f" % (-svgWidth, -svgHeight, svgWidth, svgHeight))
    root.set("width", str(svgWidth))
    root.set("height", str(svgHeight))

    path_length = self.paths[0]["length"]
    style = self.createStyleElement('aqua', path_length)
    root.append(style)

    instance = etree.Element("use")
    instance.set("x", "0")
    instance.set("y", "0")
    # Need to link to classname
    instance.set("class", "aqua")
    instance.set("{%s}href" % xlink_url, "#" + name)

    root.append(instance)
    defs = etree.Element("defs")
    defs.append(self.paths[0]["path"])
    root.append(defs)

    return etree.tostring(root)
