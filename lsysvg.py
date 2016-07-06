from lsysparse import LindenmayerParse
from pathstack import PathStack
from svgpathwriter import SvgPathWriter
from svgwriter import SvgWriter
from time import time

import sys
import getopt
import json

def usage():
  print "lsysvg -input input_filename -output output_filename"

def printStreamDebug(stream):
  result = ''
  for i in stream:
    result += str(i)
  print result

def processGrammar(configs):
  paths = [];
  for config in configs['path']:
    lindenmayerParse = LindenmayerParse(config['iterations'], config['axiom'], config['rules'])

    tSysStart = time()
    stream = lindenmayerParse.iterate()
    tSysEnd = time()
    print '  ' + str((tSysEnd - tSysStart) * 1000) + 'ms to generate l-system.'

    #printStreamDebug(stream)

    tPathStart = time()
    pathStack = PathStack(config['angle'],
                          config['length'],
                          config['length_growth'],
                          config['angle_growth'],
                          stream)
    #TODO(bradleybossard): Rename this call
    path = pathStack.toPaths()
    tPathEnd = time()
    paths.append(path)
    print '  ' + str((tPathEnd - tPathStart) * 1000) + 'ms to construct path.'
  return paths


def main(argv):
  try:
    opts, args = getopt.getopt(argv, "hio:", ["help", "input=", "output="])

  except getopt.GetoptError as err:
    print err
    sys.exit(2)

  tStart = time()

  inputFile = None
  outputFile = None

  # TODO(bradleybossard) : Add option for toggling timing info on/off
  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit(0)
    elif o in ("-i", "--input"):
      print 'ai=' + a
      inputFile = a;
    elif o in ("-o", "--output"):
      print 'ao=' + a
      outputFile = a;

  if inputFile == None:
    print "Input file missing ..."
    usage()
    sys.exit(2)

  if outputFile == None:
    print "Output file missing ..."
    usage()
    sys.exit(2)

  # Read the whole input file.
  configs = {}
  with open(inputFile, 'r') as fp:
    inputStream = fp.read()
    configs = json.loads(inputStream)
    name = configs['name']

  paths = processGrammar(configs)

  svgPathWriter = SvgPathWriter(name, paths)
  svgPath = svgPathWriter.render()
  svgPaths = []
  svgPaths.append(svgPath)

  svgWriter = SvgWriter(svgPaths)
  svgElement = svgWriter.toSvg(name)

  with open(outputFile, 'w') as fp:
    fp.write(svgElement)
  tEnd = time()
  print str((tEnd - tStart) * 1000) + 'ms to run program.'

if __name__ == "__main__":
  main(sys.argv[1:])
