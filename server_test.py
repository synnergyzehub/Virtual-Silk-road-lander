from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        message = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Simple Python HTTP Server</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    line-height: 1.6;
                }
                h1 {
                    color: #333;
                }
                .container {
                    border: 1px solid #ddd;
                    padding: 20px;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Python HTTP Server Test</h1>
                <p>This is a simple test server to verify port availability.</p>
                <p>The server is running successfully!</p>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(bytes(message, "utf8"))
        return

def run_server(port=8080):
    print(f"Starting server on port {port}...")
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f"Server running at http://0.0.0.0:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server(port=8080)