import sys, time, os, SimpleHTTPServer, SocketServer

PORT = int(sys.argv[1])
LOGFILE = sys.argv[2]

# Computes current system time in millis
current_milli_time = lambda: int(round(time.time() * 1000))

def do_GET(self):
  self.t1 = current_milli_time()
  self.send_response(200)
  self.send_header("Content-type", "text/html")
  self.end_headers()
  self.wfile.write("<html>Welcome to myCompany!</html>")

def log_message(self, format, *args): 
  t2 = current_milli_time()
  open(LOGFILE, "a").write("%s\t%s\t%s\t%s\t%s\n" %  (self.log_date_time_string(), 'web-static', str(current_milli_time() - self.t1), self.client_address[0],  format%args)) 

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
Handler.do_GET = do_GET
Handler.log_message = log_message

httpd = SocketServer.TCPServer(("", PORT), Handler)
httpd.serve_forever()
