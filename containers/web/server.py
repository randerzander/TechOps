import sys
import SimpleHTTPServer
import SocketServer

PORT = int(sys.argv[1])
LOGFILE = sys.argv[2]

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

def log_message(self, format, *args): 
  open(LOGFILE, "a").write("%s\t%s\t%s\n" %  (self.log_date_time_string(), self.client_address[0],  format%args)) 

Handler.log_message = log_message

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
