import sys
import getopt
import json
import pprint

from lsysparse import lsystem
from pathstack import PathStack
from svgpathwriter import SvgPathWriter
from svgwriter import SvgWriter

debug = False

def usage():
    print "lsysvg -input input_filename -output output_filename"

def process_grammar(configs):
    pp = pprint.PrettyPrinter(indent=4)
    paths = []
    system = lsystem(configs['iterations'], configs['axiom'], configs['rules'])
    stream = system.iterate()
    name = configs['name']
    for config in configs['path']:
        path_stack = PathStack()
        path = path_stack.toPaths(config['angle'], config['length'],
                                  config['length_growth'],
                                  config['angle_growth'], stream)
        if debug is True:
            pp.pprint(path)
        paths.append(path)

    svg_path_writer = SvgPathWriter(name, paths, configs)
    svgPath = svg_path_writer.render()
    svgPaths = []
    svgPaths.append(svgPath)

    svgWriter = SvgWriter(svgPaths, configs)
    svgElement = svgWriter.toSvg(name)
    return svgElement

def main(argv):
    global debug
    try:
        opts, args = getopt.getopt(argv, "hio:", ["help", "input=", "output=", "debug"])

    except getopt.GetoptError as err:
        print err
        sys.exit(2)

    input_file = None
    output_file = None

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-d", "--debug"):
            debug = True
        elif o in ("-i", "--input"):
            input_file = a
        elif o in ("-o", "--output"):
            output_file = a

    if input_file is None:
        print "Input file missing ..."
        usage()
        sys.exit(2)

    if output_file is None:
        print "Output file missing ..."
        usage()
        sys.exit(2)

    # Read the whole input file.
    configs = {}
    with open(input_file, 'r') as fp:
        input_stream = fp.read()
        configs = json.loads(input_stream)

        svg_string = process_grammar(configs)

    with open(output_file, 'w') as fp:
        fp.write(svg_string)

if __name__ == "__main__":
    main(sys.argv[1:])
