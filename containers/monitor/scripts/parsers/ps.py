import json

attributes = ['filename', 's2s.host']

def parse(data):
  unix_timestamp = int(data['filename'][0:13])
  lines = data['content'].split('\n')

  #Extract list of field names
  fields = lines[0].replace('%', '').split()
  fields = ['user', 'pid', 'cpu', 'mem', 'vsz', 'rss', 'tty', 'stat', 'start', 'time', 'command']

  processes = []
  for line in lines[1:]:
    tokens = line.split()
    if len(tokens) == 0: continue

    tokens = tokens[0:10] + [' '.join(tokens[10:])]
    process = {'unix_timestamp': unix_timestamp, 'host': data['s2s.host']}
    for idx, field in enumerate(fields):
      if field == 'cpu' or field == 'mem': process[field] = float(tokens[idx])
      elif field == 'vsz' or field == 'rss': process[field] = int(tokens[idx])
      else: process[field] = tokens[idx]
    processes.append(json.dumps(process))

  return '\n'.join(processes)
