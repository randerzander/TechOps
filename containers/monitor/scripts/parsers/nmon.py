import json, time
from datetime import datetime

attributes = ['s2s.host']

def extract(content, prefix, suffix='\n'):
  return content.split(prefix)[1].split(suffix)[0].strip()

def unixtime(str_dt, dt_format):
  return int(time.mktime(datetime.strptime(str_dt, dt_format).timetuple()))

def parse(data):
  content = data['content']
  host = {'hostname': data['s2s.host']}

  # Extract datetime
  str_dt = extract(content, 'AAA,time,') + ' ' + extract(content, 'AAA,date,')
  host['unix_timestamp'] = unixtime(str_dt, '%H:%M.%S %d-%b-%Y')

  # Extract host meta
  host['os'] = extract(content, '001,/etc/release').replace(',', '').replace('"', '')
  host['boot_time'] = unixtime(extract(content, 'AAA,boottime,'), '%H:%M %p %d-%b-%Y')
  host['cpu_count'] = int(extract(content, 'AAA,cpus,'))
  host['cpu_type'] = extract(content, 'ModelName,')

  # Extract current temporal metrics
  cpu = content.split('CPU_ALL')[2].split('\n')[0].split(',')
  host['cpu_user'] = float(cpu[2])
  host['cpu_sys'] = float(cpu[3])

  host['mem_free'] = int(extract(content, 'MemFree:', 'kB'))
  host['mem_avail'] = int(extract(content, 'MemAvailable:', 'kB'))
  host['mem_total'] = int(extract(content, 'MemTotal:', 'kB'))

  host['disk_busy'] = float(content.split('DISKBUSY,')[2].split(',')[1])
  host['disk_read'] = float(content.split('DISKREAD,')[2].split(',')[1])
  host['disk_write'] = float(content.split('DISKWRITE,')[2].split(',')[1])
  host['disk_xfer'] = float(content.split('DISKXFER,')[2].split(',')[1])

  return json.dumps(host)
