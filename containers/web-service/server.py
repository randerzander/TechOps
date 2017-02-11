import sys, time, os, SimpleHTTPServer, SocketServer, random

PORT = int(sys.argv[1])
LOGFILE = sys.argv[2]

# Computes CPU utilization
last_worktime=0
last_idletime=0
def get_cpu():
	global last_worktime, last_idletime
	f=open("/proc/stat","r")
	line=""
	while not "cpu " in line: line=f.readline()
	f.close()
	spl=line.split(" ")
	worktime=int(spl[2])+int(spl[3])+int(spl[4])
	idletime=int(spl[5])
	dworktime=(worktime-last_worktime)
	didletime=(idletime-last_idletime)
	rate=float(dworktime)/(didletime+dworktime)
	last_worktime=worktime
	last_idletime=idletime
	if(last_worktime==0): return 0
	return rate

# Computes current system time in millis
current_milli_time = lambda: int(round(time.time() * 1000))

t1 = current_milli_time()
def do_GET(self):
  self.t1 = current_milli_time()
  self.send_response(200)
  self.send_header("Content-type", "text/html")
  self.end_headers()
  # Simulate db lookup latency
  # Sleep for a few seconds as a function of CPU usage. Max 9 second sleep, minimum 1
  time.sleep(min(9, max(get_cpu()*3000, 1)))
  self.wfile.write("<html>Your balance is: "+str(1000*random.randint(0,9))+"</html>")

def log_message(self, format, *args): 
  open(LOGFILE, "a").write("%s\t%s\t%s\t%s\t%s\n" %  (self.log_date_time_string(), 'web-service', str(current_milli_time() - self.t1), self.client_address[0],  format%args)) 

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
Handler.log_message = log_message
Handler.do_GET = do_GET

httpd = SocketServer.TCPServer(("", PORT), Handler)
httpd.serve_forever()
