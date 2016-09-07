import sys
import getopt
import json
#import pprint

from lsysparse import lsystem
from pathstack import PathStack
from svgpathwriter import SvgPathWriter
from svgwriter import SvgWriter

def usage():
    print "lsysvg -input input_filename -output output_filename"

def process_grammar(configs):
    #pp = pprint.PrettyPrinter(indent=4)
    paths = []
    system = lsystem(configs['iterations'], configs['axiom'], configs['rules'])
    stream = system.iterate()
    name = configs['name']
    for config in configs['path']:
        path_stack = PathStack()
        path = path_stack.toPaths(config['angle'], config['length'],
                                  config['length_growth'],
                                  config['angle_growth'], stream)
        paths.append(path)

    svg_path_writer = SvgPathWriter(name, paths)
    svgPath = svg_path_writer.render()
    svgPaths = []
    svgPaths.append(svgPath)

    svgWriter = SvgWriter(svgPaths)
    svgElement = svgWriter.toSvg(name)
    return svgElement

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hio:", ["help", "input=", "output="])

    except getopt.GetoptError as err:
        print err
        sys.exit(2)

    input_file = None
    output_file = None

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-i", "--input"):
            print 'ai=' + a
            input_file = a
        elif o in ("-o", "--output"):
            print 'ao=' + a
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
