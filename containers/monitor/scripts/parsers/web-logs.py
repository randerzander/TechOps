import json, time
from datetime import datetime

attributes = ['filename', 's2s.host']

def unixtime(str_dt, dt_format):
  return int(time.mktime(datetime.strptime(str_dt, dt_format).timetuple()))

def parse(data):
  lines = data['content'].split('\n')
  requests = []
  for line in lines:
    tokens = line.split()
    if len(tokens) == 0: continue
    requests.append(json.dumps({
      'hostname': data['s2s.host'],
      'unix_timestamp': unixtime(tokens[0] + ' ' + tokens[1], '%d/%b/%Y %H:%M:%S'),
      'app': tokens[2],
      'response_time': float(tokens[3]),
      'src_ip': tokens[4],
      'http_code': tokens[-2],
      'url': ' '.join(tokens[5:-2]).replace('"', '').strip()
    }))
  return '\n'.join(requests)
