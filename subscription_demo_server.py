"""
Subscription Demo Server for Empire OS

This server provides an HTML-based demo of the Empire OS subscription model,
showcasing data flow visualization from factory to consumer.
"""

import http.server
import socketserver
import os
import json
from datetime import datetime, timedelta
import uuid

# Define the port to serve on
PORT = 8080

# Create data directories if they don't exist
os.makedirs('data/subscriptions', exist_ok=True)
os.makedirs('data/flow_data', exist_ok=True)
os.makedirs('data/leads', exist_ok=True)


class SubscriptionDemoHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for the subscription demo server"""
    
    def do_GET(self):
        """Handle GET requests"""
        # Set default path to the subscription demo page
        if self.path == '/':
            self.path = '/static/subscription_demo.html'
            
        # Handle API requests for subscription data
        elif self.path.startswith('/api/'):
            return self.handle_api_request()
            
        # Serve the requested file
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        """Handle POST requests"""
        # API endpoint for contact form submissions
        if self.path == '/api/contact':
            return self.handle_contact_submission()
        
        # API endpoint for subscription changes
        elif self.path == '/api/subscription/change':
            return self.handle_subscription_change()
            
        # Return 404 for other POST requests
        self.send_error(404, "Not Found")
    
    def handle_api_request(self):
        """Handle API GET requests"""
        # API endpoint for subscription info
        if self.path == '/api/subscription/info':
            # In a real app, this would lookup the subscription from a database
            response = {
                'client_id': 'DEMO12345',
                'tier': 'free_demo',
                'start_date': (datetime.now() - timedelta(days=7)).isoformat(),
                'expiry_date': (datetime.now() + timedelta(days=23)).isoformat(),
                'status': 'active'
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return True
            
        # Return 404 for other API requests
        self.send_error(404, "API endpoint not found")
        return True
    
    def handle_contact_submission(self):
        """Handle contact form submissions"""
        # Get the content length
        content_length = int(self.headers['Content-Length'])
        
        # Read the POST data
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse the JSON data
            form_data = json.loads(post_data.decode())
            
            # In a real app, this would save to a database and send notifications
            lead_data = {
                'timestamp': datetime.now().isoformat(),
                'company_name': form_data.get('company_name', ''),
                'contact_name': form_data.get('contact_name', ''),
                'email': form_data.get('email', ''),
                'phone': form_data.get('phone', ''),
                'interested_tier': form_data.get('tier', ''),
                'message': form_data.get('message', '')
            }
            
            # Save the lead data to a file (for demonstration purposes)
            lead_id = uuid.uuid4().hex[:8]
            with open(f'data/leads/lead_{lead_id}.json', 'w') as f:
                json.dump(lead_data, f, indent=2)
                
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                'success': True,
                'message': 'Thank you for your interest! Our ECG licensing team will contact you shortly.'
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except json.JSONDecodeError:
            # Send error response for invalid JSON
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                'success': False,
                'message': 'Invalid request format.'
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        return True
    
    def handle_subscription_change(self):
        """Handle subscription change requests"""
        # Get the content length
        content_length = int(self.headers['Content-Length'])
        
        # Read the POST data
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse the JSON data
            subscription_data = json.loads(post_data.decode())
            
            # Extract the client ID and new tier
            client_id = subscription_data.get('client_id', 'DEMO12345')
            new_tier = subscription_data.get('tier', 'free_demo')
            
            # In a real app, this would update the subscription in a database
            updated_subscription = {
                'client_id': client_id,
                'tier': new_tier,
                'start_date': datetime.now().isoformat(),
                'expiry_date': (datetime.now() + timedelta(days=30)).isoformat(),
                'status': 'active',
                'last_updated': datetime.now().isoformat()
            }
            
            # Save the updated subscription to a file (for demonstration purposes)
            with open(f'data/subscriptions/{client_id}.json', 'w') as f:
                json.dump(updated_subscription, f, indent=2)
                
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                'success': True,
                'message': f'Subscription updated to {new_tier} successfully.',
                'subscription': updated_subscription
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except json.JSONDecodeError:
            # Send error response for invalid JSON
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                'success': False,
                'message': 'Invalid request format.'
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        return True


def run_server():
    """Run the subscription demo server"""
    with socketserver.TCPServer(("", PORT), SubscriptionDemoHandler) as httpd:
        print(f"Serving at http://0.0.0.0:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    run_server()