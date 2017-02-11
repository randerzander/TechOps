import json

attributes = ['filename', 's2s.host']

def parse(data):
  unix_timestamp = data['filename'][0:13]

  # Active Internet connections
  lines = data['content'].split('Active UNIX')[0].split('\n')
  fields = ['proto', 'recv_q', 'send_q', 'local_address', 'foreign_address', 'state', 'user', 'inode', 'pid', 'program']
  connections = []
  for line in lines[2:]:
    # Replace '/' in PID/Program Name to space to split into two fields
    line = line.replace('/', ' ', 1)
    tokens = line.split()
    if len(tokens) == 0: continue
    # udp connections lack state
    if tokens[0] == 'udp': tokens = tokens[0:5] + [''] + tokens[5:]
    # Replace '-' in PID/Program Name to space to ensure two blank fields
    if tokens[-1] == '-': tokens = tokens[0:-1] + ['', '']

    connection = {'traffic_type': 'internet', 'unix_timestamp': unix_timestamp, 'host': data['s2s.host']}
    for idx, field in enumerate(fields):
      if field == 'recv_q' or field == 'send_q': connection[field] = int(tokens[idx])
      else: connection[field] = tokens[idx]
    connections.append(json.dumps(connection))
  
  # Active UNIX domain sockets
  lines = data['content'].split('Active UNIX')[1].split('\n')
  fields = ['proto', 'refcnt', 'flags', 'type', 'state', 'inode', 'pid', 'program', 'path']

  for line in lines[2:]:
    # Remove square brackets in flags list
    line = line.replace('[', '').replace(']', '')
    # Replace '/' in PID/Program Name to space to split into two fields
    line = line.replace('/', ' ', 1)
    tokens = line.split()
    if len(tokens) == 0: continue
    # Replace '-' in PID/Program Name to space to ensure two blank fields
    if tokens[-2] == '-': tokens = tokens[0:-1] + ['', '']

    connection = {'traffic_type': 'unix_socket', 'unix_timestamp': unix_timestamp, 'host': data['s2s.host']}
    for idx, field in enumerate(fields):
      if field == 'refcnt': connection[field] = int(tokens[idx])
      else: connection[field] = tokens[idx]
    connections.append(json.dumps(connection))
  return '\n'.join(connections)
