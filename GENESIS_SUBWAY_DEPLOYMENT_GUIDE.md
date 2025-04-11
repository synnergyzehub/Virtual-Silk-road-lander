# Genesis Subway Deployment Guide

This guide describes how to deploy and manage the Genesis Stack using the "subway" deployment model, where each entity operates on its own isolated "track" while sharing the core infrastructure.

## Architecture Overview

```
                   ┌─────────────────────────────────────┐
                   │                                     │
                   │       CENTRAL STATION               │
                   │    (Genesis Coordination System)    │
                   │                                     │
                   └───────────────┬─────────────────────┘
                                   │
                   ┌───────────────┼─────────────────────┐
                   │               │                     │
┌──────────────────▼──┐  ┌─────────▼────────┐  ┌────────▼──────────┐
│                     │  │                  │  │                   │
│     TRACK 1         │  │     TRACK 2      │  │     TRACK 3       │
│  (Entity Subway)    │  │  (Entity Subway) │  │  (Entity Subway)  │
│                     │  │                  │  │                   │
└─────────┬───────────┘  └────────┬─────────┘  └─────────┬─────────┘
          │                       │                      │
┌─────────▼───────────┐  ┌────────▼─────────┐  ┌─────────▼─────────┐
│                     │  │                  │  │                   │
│    NPU NODE 1       │  │    NPU NODE 2    │  │    NPU NODE 3     │
│ (Governance Engine) │  │ (Governance Engine│  │ (Governance Engine│
│                     │  │                  │  │                   │
└─────────────────────┘  └──────────────────┘  └───────────────────┘
```

## Component Overview

1. **Central Station** - The coordination system that manages all Genesis Stack services
2. **Entity Subway Tracks** - Isolated entity-specific configurations and deployments
3. **NPU Nodes** - Neural Processing Units that enforce computational governance rules

## Deployment Process

### 1. Start the Central Station

The Central Station manages all services and provides a unified interface:

```bash
# Start all services
python run_central_station.py

# Start with a specific entity configuration
python run_central_station.py --entity MyOrganization

# Start only the Genesis Shell
python run_central_station.py --shell-only

# Check status of running services
python run_central_station.py --status
```

### 2. Register NPU Nodes

NPU nodes provide the computational governance infrastructure:

```bash
# Register a new NPU node
python tools/register_npu_node.py --node-id "NPU-001" --region "IND-KA" --entities "MyOrganization"

# Initialize governance rules for the NPU node
python tools/init_npu_governance.py --node-id "NPU-001" --ecg-key "emperorkey123"
```

### 3. Generate SynergyzeOS Licenses

Licenses control entity access to the system:

```bash
# Generate a new license for an entity
python tools/generate_synergyze_license.py --entity "MyOrganization" --modules "commerce,governance,identity" --term "annual"

# Assign the license to an NPU node
python tools/assign_license_to_npu.py --license "SYN-MYORG-230411" --node-id "NPU-001"
```

### 4. Manage Entities through Genesis Shell

The Genesis Shell provides an indexed interface for managing all components:

```bash
# Start the Genesis Shell interface
python run_genesis_shell_terminal.py
```

## Subway Configuration

Each entity subway track has its own configuration:

- **Port allocation**: Each entity gets its own port range
  - License API: 5x01 (e.g., 5101, 5201, 5301)
  - License Management: 8x05 (e.g., 8105, 8205, 8305)
  - Welcome Server: 8x90 (e.g., 8190, 8290, 8390)

- **Directory structure**:
  ```
  config/
  ├── entity-1/
  │   ├── entity.json
  │   ├── ports.json
  │   └── services.json
  ├── entity-2/
  │   ├── entity.json
  │   ├── ports.json
  │   └── services.json
  ```

- **Data isolation**:
  ```
  data/
  ├── licenses/
  │   ├── SYN-ENT1-230411.json
  │   └── SYN-ENT2-230411.json
  ├── npu_nodes/
  ├── governance_rules/
  ├── divine_filters/
  └── license_assignments/
  ```

## NPU-SynergyzeOS Integration

The NPU nodes use SynergyzeOS licensing to enforce computational governance:

1. NPU nodes register with the Central Station
2. Entities are assigned to NPU nodes
3. SynergyzeOS licenses control what operations an entity can perform
4. Divine Alignment Layer ensures ethical compliance
5. Governance rules enforce organizational policies

## Managing the System

### Indexed Component Interface

The Genesis Shell provides a paginated workflow for all components:

- Filter by component type: licenses, NPU nodes, governance rules, etc.
- Search by ID, name, or other attributes
- View detailed component information
- Manage component relationships

### Service Management

The Central Station provides tools for managing services:

- Start/stop individual services
- Monitor service health
- View logs and diagnostics
- Coordinate service interactions

## Core Commands

```bash
# Start the complete stack
python run_central_station.py

# View system status
python run_central_station.py --status

# Access the Genesis Shell interface
python run_genesis_shell_terminal.py

# Register a new entity
python tools/onboard_entity.py --name "NewEntity" --region "US-CA"

# Register a new NPU node
python tools/register_npu_node.py --node-id "NPU-002" --region "US-CA" --entities "NewEntity"
```

---

For more detailed information, refer to:
- NPU_SYNERGYZE_DEPLOYMENT.md - Details on NPU node deployment
- tools/genesis_shell_terminal.py - Documentation on indexed shell commands
- genesis_workflows.py - Workflow configuration options