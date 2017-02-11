from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import os, sys, imp, traceback, time

#parser_path = '/Users/randy/projects/TechOps/containers/monitor/scripts/parsers/'
parser_path = '/scripts/parsers/'

class PyStreamCallback(StreamCallback):
  def __init__(self, result):
    self.result = result
  def process(self, instream, outstream):
    outstream.write(self.result)

def fail(flowfile, err):
  flowfile = session.putAttribute(flowfile, 'parse.error', err)
  session.transfer(flowfile, REL_FAILURE)

def process(flowfile):
  parser = flowfile.getAttribute('parser')
  path = parser_path + parser + '.py'
  # load the parser if it has been updated
  if parser not in sys.modules or os.path.getmtime(path) > sys.modules[parser].loaded_at:
    try:
      module = imp.load_source(parser, path)
      module.loaded_at = int(time.time())
    except:
      fail(flowfile, 'Loading Module: ' + traceback.format_exc())
      return
  parse_module = sys.modules[parser]

  # Read flowfile content
  data = {}
  instream = session.read(flowfile)
  if hasattr(parse_module, 'format') and parse_module.format.lower() == 'binary':
    data['content'] = IOUtils.toByteArray(instream)
  else:
    data['content'] = IOUtils.toString(instream, StandardCharsets.UTF_8)
  instream.close()

  # Attempt to parse
  try:
    if hasattr(parse_module, 'attributes'):
      for attribute in parse_module.attributes:
        data[attribute] = flowfile.getAttribute(attribute)
    result = parse_module.parse(data)
    flowfile = session.write(flowfile, PyStreamCallback(result))
    session.transfer(flowfile, REL_SUCCESS)
  except:
    fail(flowfile, 'Parsing: ' + traceback.format_exc())

# Execution starts here
flowfile = session.get()
if (flowfile != None): process(flowfile)
