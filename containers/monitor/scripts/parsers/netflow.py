import socket, struct, json, imp

imp.load_source('netflow_v9', '/scripts/parsers/netflow_v9.py')
from netflow_v9 import *

def to_string(ip):
  return ".".join(map(lambda n: str(ip>>n & 0xFF), [24,16,8,0]))

def get_hostname(ip):
  try:
    hostname = socket.gethostbyaddr(ip)[0]
    # Uncomment to remove docker's hostname prefix and suffix
    #if '_' in hostname: return hostname.split('_')[1]
    #else: return hostname
    return hostname
  except Exception,e:
    return None

def process_v9(data):
    export = ExportPacket(data, _templates)
    _templates.update(export.templates)

    ret = []
    for idx, flow in enumerate(export.flows):
      src_ip = to_string(flow.data['IPV4_SRC_ADDR'])
      dst_ip = to_string(flow.data['IPV4_DST_ADDR'])
      flow.data['IPV4_SRC_ADDR'] = src_ip
      flow.data['IPV4_DST_ADDR'] = dst_ip
      if src_ip != '192.168.1.1' and dst_ip != '192.168.1.1':
        flow.data['IPV4_SRC_HOSTNAME'] = get_hostname(src_ip)
        flow.data['IPV4_DST_HOSTNAME'] = get_hostname(dst_ip)
        ret.append(json.dumps(flow.data))
    return ret

# based on: http://blog.devicenull.org/2013/09/04/python-netflow-v5-parser.html
V5_HEADER_BYTES = 24
V5_RECORD_BYTES = 48
def process_v5(buf, count):
    ret = []
    try:
      for i in range(0, count):
        base = V5_HEADER_BYTES + (i * V5_RECORD_BYTES)
        data = struct.unpack('!IIIIHH',buf[base+16:base+36])
        src_ip = socket.inet_ntoa(buf[base+0:base+4])
        dst_ip = socket.inet_ntoa(buf[base+4:base+8])
        if src_ip != '192.168.1.1' and dst_ip != '192.168.1.1':
          ret.append({
            'IPV4_SRC_ADDR': src_ip, 'IPV4_DST_ADDR': dst_ip,
            'IPV4_SRC_HOSTNAME': get_hostname(src_ip), 'IPV4_DST_HOSTNAME': get_hostname(dst_ip),
            'IN_PKTS': data[0], 'IN_BYTES': data[1],
            'FIRST_SWITCHED': data[2], 'LAST_SWITCHED': data[3],
            'L4_SRC_PORT': data[4], 'L4_DST_PORT': data[5],
            'PROTOCOL': buf[base+38]
          })
    except Exception,e:
      ret.append(str(e))
    return ret

# We need to save the templates our NetFlow device send over time. Templates
# are not resent every time a flow is sent to the collector.
_templates = {}

format = 'binary'

def parse(data):
  (version, count) = struct.unpack('!HH',data['content'][0:4])
  if version == 5: results = process_v5(data['content'], count)
  elif version == 9: results = process_v9(data['content'])
  return '\n'.join(results)
