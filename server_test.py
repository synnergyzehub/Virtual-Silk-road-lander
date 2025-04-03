from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>Test Server</h1><p>This is a test server.</p></body></html>')

def run_server(port=8080):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)