import sys
import SimpleHTTPServer
import SocketServer
import time
from random import randint

PORT = int(sys.argv[1])
LOGFILE = sys.argv[2]

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

def do_get(s):
  time.sleep(7)
  s.send_response(200)
  s.send_header("Content-type", "text/html")
  s.end_headers()
  s.wfile.write("<html>Your balance is: "+str(1000*randint(0,9))+"</html>")

def log_message(self, format, *args): 
  open(LOGFILE, "a").write("%s\t%s\t%s\n" %  (self.log_date_time_string(), self.client_address[0],  format%args)) 

Handler.log_message = log_message

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
