import http.server
import socketserver
import os

PORT = 8080

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Default to welcome.html if the path is root
        if self.path == '/':
            self.path = '/static/welcome.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Make sure the static directory exists
os.makedirs('static', exist_ok=True)

handler_object = MyHttpRequestHandler
my_server = socketserver.TCPServer(("0.0.0.0", PORT), handler_object)

print(f"Server started on port {PORT}")
print(f"Access it at http://0.0.0.0:{PORT}")

my_server.serve_forever()