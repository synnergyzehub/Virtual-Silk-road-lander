#!/usr/bin/env python3
"""
Entity Onboarding Tool

This script creates and onboards a new entity in the Genesis Stack,
setting up the necessary configuration files and directory structure.
"""

import os
import sys
import json
import argparse
import random
import hashlib
import secrets
from datetime import datetime

def generate_entity_id(name, region):
    """Generate a unique entity ID."""
    base = name[:4].upper()
    region_code = region.replace("-", "")[:4].upper()
    timestamp = datetime.now().strftime("%y%m%d")
    return f"ENT-{base}-{region_code}-{timestamp}"

def calculate_ports(entity_id):
    """Calculate the ports for the entity based on its ID."""
    # Generate a deterministic number from entity_id
    hash_obj = hashlib.md5(entity_id.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    
    # Use the hash to generate a port multiplier (1-9)
    port_multiplier = (hash_int % 9) + 1
    
    # Calculate the ports
    license_api_port = 5000 + (port_multiplier * 100) + 1  # 5x01 format
    license_management_port = 8000 + (port_multiplier * 100) + 5  # 8x05 format
    welcome_server_port = 8000 + (port_multiplier * 100) + 90  # 8x90 format
    dashboard_port = 5000 + (port_multiplier * 100) + 50  # 5x50 format
    
    return {
        "license_api": license_api_port,
        "license_management": license_management_port,
        "welcome_server": welcome_server_port,
        "dashboard": dashboard_port
    }

def create_entity_files(name, region, logo_url=None, description=None):
    """Create the entity configuration files."""
    # Generate entity ID
    entity_id = generate_entity_id(name, region)
    
    # Calculate ports
    ports = calculate_ports(entity_id)
    
    # Create entity directory
    entity_dir_name = name.lower().replace(' ', '-')
    entity_dir = os.path.join("config", entity_dir_name)
    os.makedirs(entity_dir, exist_ok=True)
    
    # Create entity.json
    entity_data = {
        "entity_id": entity_id,
        "entity_name": name,
        "region": region,
        "created_at": datetime.now().isoformat(),
        "api_key": f"ent-{secrets.token_urlsafe(16)}",
        "status": "active",
        "logo_url": logo_url,
        "description": description or f"{name} organization in {region} region"
    }
    
    entity_file = os.path.join(entity_dir, "entity.json")
    with open(entity_file, 'w') as f:
        json.dump(entity_data, f, indent=2)
    
    # Create ports.json
    ports_file = os.path.join(entity_dir, "ports.json")
    with open(ports_file, 'w') as f:
        json.dump(ports, f, indent=2)
    
    # Create services.json
    services_data = {
        "license_api": {
            "command": f"python run_license_api.py --entity {entity_id} --port {ports['license_api']}",
            "port": ports['license_api'],
            "log_file": f"logs/{entity_dir_name}/license_api.log"
        },
        "license_management": {
            "command": f"python run_license_management.py --entity {entity_id} --port {ports['license_management']}",
            "port": ports['license_management'],
            "log_file": f"logs/{entity_dir_name}/license_management.log"
        },
        "welcome_server": {
            "command": f"python web_server.py --entity {entity_id} --port {ports['welcome_server']}",
            "port": ports['welcome_server'],
            "log_file": f"logs/{entity_dir_name}/welcome_server.log"
        },
        "dashboard": {
            "command": f"streamlit run genesis_dashboard.py --server.port {ports['dashboard']} -- --entity {entity_id}",
            "port": ports['dashboard'],
            "log_file": f"logs/{entity_dir_name}/dashboard.log"
        }
    }
    
    services_file = os.path.join(entity_dir, "services.json")
    with open(services_file, 'w') as f:
        json.dump(services_data, f, indent=2)
    
    # Create logs directory
    logs_dir = os.path.join("logs", entity_dir_name)
    os.makedirs(logs_dir, exist_ok=True)
    
    return {
        "entity_id": entity_id,
        "entity_dir": entity_dir,
        "entity_file": entity_file,
        "ports_file": ports_file,
        "services_file": services_file,
        "ports": ports
    }

def generate_launch_script(entity_info):
    """Generate a launch script for the entity."""
    entity_dir_name = os.path.basename(entity_info["entity_dir"])
    script_path = os.path.join(entity_info["entity_dir"], "launch.py")
    
    script_content = f"""#!/usr/bin/env python3
\"\"\"
Launch Script for {entity_info["entity_id"]}

This script launches all services for the {entity_dir_name} entity.
\"\"\"

import os
import sys
import json
import subprocess
import signal
import time

def main():
    \"\"\"Main function to launch entity services.\"\"\"
    print("Launching services for {entity_info["entity_id"]}...")
    
    # Load services configuration
    with open("{entity_info["services_file"]}", 'r') as f:
        services = json.load(f)
    
    # Start each service
    processes = []
    for service_name, service in services.items():
        print(f"Starting {service_name}...")
        
        # Ensure log directory exists
        log_file = service.get("log_file")
        if log_file:
            log_dir = os.path.dirname(log_file)
            os.makedirs(log_dir, exist_ok=True)
            
            # Open log file
            log_redirect = open(log_file, "w")
        else:
            log_redirect = None
        
        # Start process
        cmd = service["command"].split()
        process = subprocess.Popen(
            cmd,
            stdout=log_redirect,
            stderr=subprocess.STDOUT if log_redirect else None
        )
        
        processes.append((service_name, process, log_redirect))
        print(f"{service_name} started with PID {process.pid}")
    
    # Register signal handlers
    def signal_handler(sig, frame):
        print("\\nShutting down services...")
        for name, process, log_file in processes:
            print(f"Stopping {name}...")
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"{name} stopped.")
            except subprocess.TimeoutExpired:
                print(f"{name} did not terminate gracefully, killing...")
                process.kill()
            except Exception as e:
                print(f"Error stopping {name}: {e}")
            
            # Close log file if it's open
            if log_file:
                log_file.close()
        
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Keep script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
"""
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make the script executable
    os.chmod(script_path, 0o755)
    
    return script_path

def generate_deployment_guide(entity_info):
    """Generate a deployment guide for the entity."""
    entity_dir_name = os.path.basename(entity_info["entity_dir"])
    guide_path = os.path.join(entity_info["entity_dir"], "DEPLOYMENT.md")
    
    guide_content = f"""# Deployment Guide for {entity_info["entity_id"]}

This guide provides instructions for deploying and managing {entity_dir_name}.

## Port Allocation

| Service | Port |
|---------|------|
| License API | {entity_info["ports"]["license_api"]} |
| License Management | {entity_info["ports"]["license_management"]} |
| Welcome Server | {entity_info["ports"]["welcome_server"]} |
| Dashboard | {entity_info["ports"]["dashboard"]} |

## Deployment Steps

1. Start all services:
   ```bash
   python config/{entity_dir_name}/launch.py
   ```

2. Start specific services:
   ```bash
   # License API
   python run_license_api.py --entity {entity_info["entity_id"]} --port {entity_info["ports"]["license_api"]}
   
   # License Management
   python run_license_management.py --entity {entity_info["entity_id"]} --port {entity_info["ports"]["license_management"]}
   
   # Welcome Server
   python web_server.py --entity {entity_info["entity_id"]} --port {entity_info["ports"]["welcome_server"]}
   
   # Dashboard
   streamlit run genesis_dashboard.py --server.port {entity_info["ports"]["dashboard"]} -- --entity {entity_info["entity_id"]}
   ```

3. Access services:
   - License API: http://localhost:{entity_info["ports"]["license_api"]}
   - License Management: http://localhost:{entity_info["ports"]["license_management"]}
   - Welcome Server: http://localhost:{entity_info["ports"]["welcome_server"]}
   - Dashboard: http://localhost:{entity_info["ports"]["dashboard"]}

## NPU Node Assignment

To assign an NPU node to this entity:

```bash
# Register a new NPU node
python tools/register_npu_node.py --node-id "NPU-XXX" --region "{entity_info["entity_dir"].replace("config/", "").replace("-", "").upper()}" --entities "{entity_info["entity_id"]}"

# Initialize governance rules
python tools/init_npu_governance.py --node-id "NPU-XXX" --ecg-key "emperorkey123"
```

## License Generation

To generate and assign a SynergyzeOS license:

```bash
# Generate license
python tools/generate_synergyze_license.py --entity "{entity_dir_name}" --modules "commerce,governance,identity" --term "annual"

# Assign to NPU node
python tools/assign_license_to_npu.py --license "SYN-XXXX-XXXX" --node-id "NPU-XXX"
```

## Monitoring

To monitor the services:

```bash
# Check service status
python run_central_station.py --status

# View logs
tail -f logs/{entity_dir_name}/*.log
```

For more information, refer to the main Genesis Subway Deployment Guide.
"""
    
    with open(guide_path, 'w') as f:
        f.write(guide_content)
    
    return guide_path

def main():
    """Main function to run the entity onboarding script."""
    parser = argparse.ArgumentParser(description='Create and onboard a new entity in the Genesis Stack.')
    parser.add_argument('--name', required=True, help='Entity name')
    parser.add_argument('--region', required=True, help='Entity region code (e.g., US-CA, IND-KA)')
    parser.add_argument('--logo', help='URL to entity logo')
    parser.add_argument('--description', help='Entity description')
    
    args = parser.parse_args()
    
    print(f"Onboarding entity: {args.name} in region {args.region}")
    
    # Create config directory if it doesn't exist
    os.makedirs("config", exist_ok=True)
    
    # Create entity files
    entity_info = create_entity_files(args.name, args.region, args.logo, args.description)
    
    # Generate launch script
    launch_script = generate_launch_script(entity_info)
    
    # Generate deployment guide
    deployment_guide = generate_deployment_guide(entity_info)
    
    print("\nEntity Onboarding Complete!")
    print(f"Entity ID: {entity_info['entity_id']}")
    print(f"Configuration Directory: {entity_info['entity_dir']}")
    print(f"Launch Script: {launch_script}")
    print(f"Deployment Guide: {deployment_guide}")
    print("\nPort Allocation:")
    for service, port in entity_info["ports"].items():
        print(f"  {service}: {port}")
    
    print("\nNext steps:")
    print(f"1. Register an NPU node: python tools/register_npu_node.py --node-id \"NPU-001\" --region \"{args.region}\" --entities \"{entity_info['entity_id']}\"")
    print(f"2. Generate a license: python tools/generate_synergyze_license.py --entity \"{args.name}\" --modules \"commerce,governance,identity\" --term \"annual\"")
    print(f"3. Launch entity services: python {launch_script}")

if __name__ == "__main__":
    main()