"""
Empire OS Web Server

This server provides a central entry point to the Empire OS application ecosystem,
handling routing between different components and interfaces.
"""

import http.server
import socketserver
import os
import urllib.parse

# Define the port to serve on
PORT = 8090

# Create necessary directories
os.makedirs('static', exist_ok=True)
os.makedirs('data', exist_ok=True)


class EmpireOSHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for the Empire OS web server"""
    
    def do_GET(self):
        """Handle GET requests with custom routing"""
        # Parse the URL
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        # Root path - show the welcome page
        if path == '/':
            self.path = '/static/welcome.html'
            
        # Subscription demo path
        elif path == '/subscription-demo/' or path == '/subscription-demo':
            self.path = '/static/subscription_demo.html'
            
        # Voi inventory path - redirect to Streamlit app on port 5000
        elif path == '/voi-inventory/' or path == '/voi-inventory':
            self.send_response(302)
            self.send_header('Location', 'http://0.0.0.0:5000')
            self.end_headers()
            return
            
        # Serve the requested file
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def run_server():
    """Run the Empire OS web server"""
    with socketserver.TCPServer(("", PORT), EmpireOSHandler) as httpd:
        print(f"Empire OS Web Server running at http://0.0.0.0:{PORT}")
        print("Available routes:")
        print("  / - Welcome page")
        print("  /subscription-demo/ - Subscription demo")
        print("  /voi-inventory/ - Voi Jeans inventory management (redirects to Streamlit)")
        
        # Start the server
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()