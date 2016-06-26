#!/usr/bin/python

class SvgWriter():
  def __init__(self, paths):
    self.paths = paths

  # TODO(bradleybossard) : Rename to render, move name to initialization.
  def toSvg(self, name):
    header = '<?xml version="1.0" standalone="no"?>\n \
              <?xml-stylesheet href="svg.css" type="text/css"?>\n \
              <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" \
                "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'

    xValues = []
    yValues = []
    for path in self.paths:
      xValues.append(path['bbox'][0]) #minX
      yValues.append(path['bbox'][1]) #minY
      xValues.append(path['bbox'][2]) #maxX
      yValues.append(path['bbox'][3]) #maxY

    minX = min(xValues)
    maxX = max(xValues)
    minY = min(yValues)
    maxY = max(yValues)

    svgWidth = str(abs(maxX - minX))
    svgHeight = str(abs(maxY - minY))

    output = '<svg\n \
       xmlns:dc="http://purl.org/dc/elements/1.1/"\n \
       xmlns:cc="http://creativecommons.org/ns#"\n \
       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n \
       xmlns:svg="http://www.w3.org/2000/svg"\n \
       xmlns="http://www.w3.org/2000/svg"\n \
       xmlns:xlink="http://www.w3.org/1999/xlink"\n \
       viewBox="0 0 ' + svgWidth + ' ' + svgHeight + '" \n \
       >\n';
       #width="' + svgWidth + '"\n \
       #height="' + svgHeight + '"\n \
       #viewBox="0 0 800 200" \n \
       #zoomAndPan="enable" \n \

    instance = '<use x="0" y="0" stroke="black" stroke-width="1" fill="none" xlink:href="#' + name + '" />\n'

    output += instance
    output += '<defs>\n' + self.paths[0]['path'] + '</defs>\n'

    output += '</svg>\n'
    return output
