#!/usr/bin/env python3
"""
Empire OS Web Server - Welcome Page

This script runs a simple web server to serve as the welcome page and entry point for
the Empire OS ecosystem. It provides links to various applications and redirects users
based on their licenses.

It also supports entity-specific configurations for multi-entity deployment.
"""

import http.server
import socketserver
import os
import json
import argparse

def load_entity_config(entity_name):
    """Load configuration for an entity."""
    entity_dir_name = entity_name.lower().replace(' ', '-')
    entity_config_dir = os.path.join('config', entity_dir_name)
    
    if not os.path.exists(entity_config_dir):
        print(f"Error: Configuration for entity '{entity_name}' not found.")
        print(f"Expected directory: {entity_config_dir}")
        return None
    
    # Load ports configuration
    ports_file = os.path.join(entity_config_dir, 'ports.json')
    if not os.path.exists(ports_file):
        print(f"Error: Ports configuration for entity '{entity_name}' not found.")
        print(f"Expected file: {ports_file}")
        return None
    
    try:
        with open(ports_file, 'r') as f:
            ports = json.load(f)
    except Exception as e:
        print(f"Error loading ports configuration: {e}")
        return None
    
    # Load entity metadata
    entity_file = os.path.join(entity_config_dir, 'entity.json')
    entity_metadata = {}
    if os.path.exists(entity_file):
        try:
            with open(entity_file, 'r') as f:
                entity_metadata = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load entity metadata: {e}")
    
    return {
        "entity_name": entity_name,
        "entity_dir_name": entity_dir_name,
        "config_dir": entity_config_dir,
        "port": ports.get("welcome_page_port", 8090),
        "entity_metadata": entity_metadata,
        "brand_portal_port": ports.get("brand_portal_port", 5000),
        "license_management_port": ports.get("license_management_port", 8505),
        "license_api_port": ports.get("license_api_port", 5001)
    }

class EmpireOSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.entity_config = kwargs.pop('entity_config', None)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        # Define routes
        routes = {
            '/': self.handle_home,
            '/subscription-demo/': self.handle_subscription_demo,
            '/voi-inventory/': self.handle_voi_inventory,
            '/license-management/': self.handle_license_management,
            '/ecg/': self.handle_ecg,
            '/brand/': self.handle_brand,
            '/tech-admin/': self.handle_tech_admin,
            '/digitalme/': self.handle_digitalme
        }
        
        # Check for exact route match
        if self.path in routes:
            routes[self.path]()
            return
        
        # Check for partial route match (e.g., /brand/voi-jeans)
        for route, handler in routes.items():
            if self.path.startswith(route) and route != '/':
                handler(self.path[len(route):])
                return
        
        # Fall back to file serving
        super().do_GET()
    
    def handle_home(self):
        """Handle requests to the home page."""
        entity_name = "Default"
        if self.entity_config and "entity_name" in self.entity_config:
            entity_name = self.entity_config["entity_name"]
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Empire OS - {entity_name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f8f9fa;
                }}
                header {{
                    background-color: #1a365d;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .card {{
                    background-color: white;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                    padding: 20px;
                }}
                .card-title {{
                    color: #1a365d;
                    border-bottom: 2px solid #ffd700;
                    padding-bottom: 10px;
                    margin-top: 0;
                }}
                .btn {{
                    display: inline-block;
                    background-color: #1a365d;
                    color: white;
                    padding: 10px 15px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-right: 10px;
                    margin-bottom: 10px;
                }}
                .btn:hover {{
                    background-color: #2a4a7f;
                }}
                footer {{
                    background-color: #1a365d;
                    color: white;
                    padding: 10px;
                    text-align: center;
                    position: fixed;
                    bottom: 0;
                    width: 100%;
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>Welcome to Empire OS</h1>
                <p>Divine Mechanics Computational System</p>
            </header>
            
            <div class="container">
                <div class="card">
                    <h2 class="card-title">Empire OS - {entity_name}</h2>
                    <p>Select an application to access:</p>
                    
                    <div>
                        <a href="/voi-inventory/" class="btn">Voi Jeans Inventory</a>
                        <a href="/license-management/" class="btn">License Management</a>
                        <a href="/ecg/" class="btn">ECG Governance</a>
                        <a href="/brand/" class="btn">Brand Portal</a>
                        <a href="/tech-admin/" class="btn">Tech Admin</a>
                        <a href="/digitalme/" class="btn">DigitalMe Console</a>
                    </div>
                </div>
                
                <div class="card">
                    <h2 class="card-title">System Information</h2>
                    <p><strong>Entity:</strong> {entity_name}</p>
        """
        
        # Add entity-specific information if available
        if self.entity_config and "entity_metadata" in self.entity_config:
            metadata = self.entity_config["entity_metadata"]
            if metadata:
                html += f"<p><strong>Entity ID:</strong> {metadata.get('entity_id', 'Unknown')}</p>\n"
                html += f"<p><strong>Created At:</strong> {metadata.get('created_at', 'Unknown')}</p>\n"
                html += f"<p><strong>Subway Line:</strong> {metadata.get('subway_line', 'Unknown')}</p>\n"
        
        # Add service endpoints
        brand_portal_port = 5000
        license_management_port = 8505
        license_api_port = 5001
        
        if self.entity_config:
            brand_portal_port = self.entity_config.get("brand_portal_port", 5000)
            license_management_port = self.entity_config.get("license_management_port", 8505)
            license_api_port = self.entity_config.get("license_api_port", 5001)
        
        html += f"""
                    <p><strong>Service Endpoints:</strong></p>
                    <ul>
                        <li>Brand Portal: <a href="http://localhost:{brand_portal_port}">http://localhost:{brand_portal_port}</a></li>
                        <li>License Management: <a href="http://localhost:{license_management_port}">http://localhost:{license_management_port}</a></li>
                        <li>License API: <a href="http://localhost:{license_api_port}">http://localhost:{license_api_port}</a></li>
                    </ul>
                </div>
            </div>
            
            <footer>
                Empire OS &copy; 2025 - Built with truth. Deployed in clarity. Governed by alignment.
            </footer>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_subscription_demo(self):
        """Handle requests to the subscription demo page."""
        self.send_response(302)
        self.send_header('Location', 'http://localhost:5000')
        self.end_headers()
    
    def handle_voi_inventory(self):
        """Handle requests to the Voi Jeans inventory management page."""
        brand_portal_port = 5000
        if self.entity_config:
            brand_portal_port = self.entity_config.get("brand_portal_port", 5000)
        
        self.send_response(302)
        self.send_header('Location', f'http://localhost:{brand_portal_port}')
        self.end_headers()
    
    def handle_license_management(self):
        """Handle requests to the license management page."""
        license_management_port = 8505
        if self.entity_config:
            license_management_port = self.entity_config.get("license_management_port", 8505)
        
        self.send_response(302)
        self.send_header('Location', f'http://localhost:{license_management_port}')
        self.end_headers()
    
    def handle_ecg(self, path=''):
        """Handle requests to the ECG governance page."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Empire OS - ECG Governance</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f8f9fa;
                }}
                header {{
                    background-color: #1a365d;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .card {{
                    background-color: white;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                    padding: 20px;
                }}
                .card-title {{
                    color: #1a365d;
                    border-bottom: 2px solid #ffd700;
                    padding-bottom: 10px;
                    margin-top: 0;
                }}
                .btn {{
                    display: inline-block;
                    background-color: #1a365d;
                    color: white;
                    padding: 10px 15px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-right: 10px;
                    margin-bottom: 10px;
                }}
                .btn:hover {{
                    background-color: #2a4a7f;
                }}
                footer {{
                    background-color: #1a365d;
                    color: white;
                    padding: 10px;
                    text-align: center;
                    position: fixed;
                    bottom: 0;
                    width: 100%;
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>ECG Governance Portal</h1>
                <p>Emperor's Computational Governance</p>
            </header>
            
            <div class="container">
                <div class="card">
                    <h2 class="card-title">ECG Governance</h2>
                    <p>The Emperor's Computational Governance (ECG) system is the central authority
                    for license issuance, validation, and oversight within the Empire OS ecosystem.</p>
                    
                    <div>
                        <a href="/license-management/" class="btn">License Management</a>
                        <a href="/" class="btn">Back to Home</a>
                    </div>
                </div>
            </div>
            
            <footer>
                Empire OS &copy; 2025 - Built with truth. Deployed in clarity. Governed by alignment.
            </footer>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_brand(self, path=''):
        """Handle requests to the brand portal."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Empire OS - Brand Portal</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f8f9fa;
                }}
                header {{
                    background-color: #1a365d;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .card {{
                    background-color: white;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                    padding: 20px;
                }}
                .card-title {{
                    color: #1a365d;
                    border-bottom: 2px solid #ffd700;
                    padding-bottom: 10px;
                    margin-top: 0;
                }}
                .btn {{
                    display: inline-block;
                    background-color: #1a365d;
                    color: white;
                    padding: 10px 15px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-right: 10px;
                    margin-bottom: 10px;
                }}
                .btn:hover {{
                    background-color: #2a4a7f;
                }}
                footer {{
                    background-color: #1a365d;
                    color: white;
                    padding: 10px;
                    text-align: center;
                    position: fixed;
                    bottom: 0;
                    width: 100%;
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>Brand Portal</h1>
                <p>Empire OS Brand Management</p>
            </header>
            
            <div class="container">
                <div class="card">
                    <h2 class="card-title">Brand Portal</h2>
                    <p>The Brand Portal allows brands to manage their inventory, operations, and
                    licenses within the Empire OS ecosystem.</p>
                    
                    <div>
                        <a href="/voi-inventory/" class="btn">Voi Jeans Inventory</a>
                        <a href="/" class="btn">Back to Home</a>
                    </div>
                </div>
            </div>
            
            <footer>
                Empire OS &copy; 2025 - Built with truth. Deployed in clarity. Governed by alignment.
            </footer>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_tech_admin(self, path=''):
        """Handle requests to the tech admin page."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Empire OS - Tech Admin</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f8f9fa;
                }}
                header {{
                    background-color: #1a365d;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .card {{
                    background-color: white;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                    padding: 20px;
                }}
                .card-title {{
                    color: #1a365d;
                    border-bottom: 2px solid #ffd700;
                    padding-bottom: 10px;
                    margin-top: 0;
                }}
                .btn {{
                    display: inline-block;
                    background-color: #1a365d;
                    color: white;
                    padding: 10px 15px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-right: 10px;
                    margin-bottom: 10px;
                }}
                .btn:hover {{
                    background-color: #2a4a7f;
                }}
                footer {{
                    background-color: #1a365d;
                    color: white;
                    padding: 10px;
                    text-align: center;
                    position: fixed;
                    bottom: 0;
                    width: 100%;
                }}
                pre {{
                    background-color: #f5f5f5;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>Tech Admin Portal</h1>
                <p>Empire OS Technical Administration</p>
            </header>
            
            <div class="container">
                <div class="card">
                    <h2 class="card-title">Tech Admin Portal</h2>
                    <p>The Tech Admin Portal allows technical administrators to manage the
                    deployment and configuration of the Empire OS ecosystem.</p>
                    
                    <h3>Stack Information</h3>
                    <pre>
Name: Genesis_Stack_v1.0_Emperor_Build
Hash: c5d12fb258b38be3f1a1c11716c72de1729b7ca0e764d2ce0b8c9f0edb56da88
                    </pre>
                    
                    <h3>Deployment Instructions</h3>
                    <pre>
# Clone the repository
git clone https://github.com/yourusername/genesis-stack.git

# Install dependencies
cd genesis-stack
pip install -r requirements.txt

# Start the License API
python run_license_api.py

# Start the License Management Interface
python run_license_management.py

# Start the Welcome Page Server
python web_server.py
                    </pre>
                    
                    <div>
                        <a href="/" class="btn">Back to Home</a>
                    </div>
                </div>
            </div>
            
            <footer>
                Empire OS &copy; 2025 - Built with truth. Deployed in clarity. Governed by alignment.
            </footer>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_digitalme(self, path=''):
        """Handle requests to the DigitalMe console."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Empire OS - DigitalMe Console</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f8f9fa;
                }}
                header {{
                    background-color: #1a365d;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .card {{
                    background-color: white;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                    padding: 20px;
                }}
                .card-title {{
                    color: #1a365d;
                    border-bottom: 2px solid #ffd700;
                    padding-bottom: 10px;
                    margin-top: 0;
                }}
                .btn {{
                    display: inline-block;
                    background-color: #1a365d;
                    color: white;
                    padding: 10px 15px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-right: 10px;
                    margin-bottom: 10px;
                }}
                .btn:hover {{
                    background-color: #2a4a7f;
                }}
                footer {{
                    background-color: #1a365d;
                    color: white;
                    padding: 10px;
                    text-align: center;
                    position: fixed;
                    bottom: 0;
                    width: 100%;
                }}
                pre {{
                    background-color: #f5f5f5;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>DigitalMe Console</h1>
                <p>Empire OS Founder's Console</p>
            </header>
            
            <div class="container">
                <div class="card">
                    <h2 class="card-title">DigitalMe Console</h2>
                    <p>The DigitalMe Console provides comprehensive oversight of the entire
                    Empire OS ecosystem for the founder.</p>
                    
                    <h3>Certificate of Sovereignty</h3>
                    <pre>
Certificate of Genesis Sovereignty

This certifies that the Genesis Stack version 1.0 (Emperor Build) has been officially launched,
registered, and archived under sovereign digital governance.

Stack Hash (SHA256):
c5d12fb258b38be3f1a1c11716c72de1729b7ca0e764d2ce0b8c9f0edb56da88

Date of Origin: 2025-04-11T07:29:37.121931Z

This certificate shall serve as a record of trust, governance, and origin, as recorded in the DigitalMe
Ledger Registry and enforced under ECG oversight.
                    </pre>
                    
                    <div>
                        <a href="/ecg/" class="btn">ECG Governance</a>
                        <a href="/brand/" class="btn">Brand Portal</a>
                        <a href="/tech-admin/" class="btn">Tech Admin</a>
                        <a href="/" class="btn">Back to Home</a>
                    </div>
                </div>
            </div>
            
            <footer>
                Empire OS &copy; 2025 - Built with truth. Deployed in clarity. Governed by alignment.
            </footer>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

def run_server(port, entity_config=None):
    """Run the web server."""
    handler = lambda *args, **kwargs: EmpireOSRequestHandler(*args, entity_config=entity_config, **kwargs)
    
    with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
        print(f"Empire OS Web Server running at http://0.0.0.0:{port}")
        print("Available routes:")
        print("  / - Welcome page")
        print("  /subscription-demo/ - Subscription demo")
        print("  /voi-inventory/ - Voi Jeans inventory management (redirects to Streamlit)")
        httpd.serve_forever()

def main():
    parser = argparse.ArgumentParser(description='Run the Empire OS Web Server.')
    parser.add_argument('--port', type=int, default=8090, help='Port to run the server on (default: 8090 or from config)')
    parser.add_argument('--entity', help='Entity name to load configuration for')
    
    args = parser.parse_args()
    
    port = args.port
    entity_config = None
    
    # If entity is specified, load configuration
    if args.entity:
        entity_config = load_entity_config(args.entity)
        if entity_config:
            port = entity_config["port"]
    
    # Override with command line arguments if provided
    if args.port:
        port = args.port
    
    run_server(port, entity_config)

if __name__ == "__main__":
    main()