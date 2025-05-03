# Voi Jeans APAC Deployment Configuration
## Synergyze Governance & Genesis Stack Implementation

**Version:** 1.0  
**Date:** April 11, 2025  
**Client:** Voi Jeans Retail India Pvt Ltd  
**Role:** IP Holder for Voi Jeans Brand (APAC Region)  
**Supplier:** Scotts Garments Ltd  
**Governance Consultant:** ECG (Emperor's Computational Governance)  
**Platform:** Synergyze with Genesis Core Stack

---

## 1. Entity Configuration

### Primary Entity: Voi Jeans Retail India Pvt Ltd
```json
{
  "entity_id": "ENT-VOI-APAC-25001",
  "legal_name": "Voi Jeans Retail India Pvt Ltd",
  "entity_type": "IP_HOLDER",
  "jurisdiction": "India",
  "region_block": "APAC",
  "region_code": "REG-APAC",
  "wto_compliance": "Developing Economy Protocol",
  "divine_alignment_factor": 0.92,
  "governance_class": "STANDARD",
  "license_tier": "PREMIUM"
}
```

### Secondary Entity: Scotts Garments Ltd
```json
{
  "entity_id": "ENT-SCOTTS-APAC-25002",
  "legal_name": "Scotts Garments Ltd",
  "entity_type": "MANUFACTURER",
  "jurisdiction": "Bangladesh",
  "region_block": "SAARC",
  "region_code": "REG-SAARC",
  "wto_compliance": "Least Developed Country Protocol",
  "divine_alignment_factor": 0.88,
  "governance_class": "STANDARD",
  "license_tier": "STANDARD",
  "relationships": [
    {
      "entity_id": "ENT-VOI-APAC-25001",
      "relationship_type": "SUPPLIER_TO",
      "contract_id": "VOI-SCOTTS-2025-001",
      "initialized_date": "2025-01-15"
    }
  ]
}
```

### Governance Entity: ECG
```json
{
  "entity_id": "ENT-ECG-GLOBAL-25000",
  "legal_name": "Emperor's Computational Governance",
  "entity_type": "GOVERNANCE_PROVIDER",
  "jurisdiction": "Global",
  "region_block": "GLOBAL",
  "region_code": "REG-GLOB",
  "divine_alignment_factor": 1.0,
  "governance_class": "EMPEROR",
  "license_tier": "ENTERPRISE",
  "relationships": [
    {
      "entity_id": "ENT-VOI-APAC-25001",
      "relationship_type": "GOVERNANCE_PROVIDER_TO",
      "contract_id": "ECG-VOI-2025-001",
      "initialized_date": "2025-01-01"
    },
    {
      "entity_id": "ENT-SCOTTS-APAC-25002",
      "relationship_type": "GOVERNANCE_PROVIDER_TO",
      "contract_id": "ECG-SCOTTS-2025-001",
      "initialized_date": "2025-01-10"
    }
  ]
}
```

## 2. Docker Deployment Configuration

### Voi Jeans Container Configuration
```yaml
# docker-compose.voi-jeans.yml
version: '3.8'

services:
  welcome-server-voi:
    image: genesis-core:latest
    container_name: voi-welcome-server
    command: python web_server.py
    ports:
      - "8190:8090"  # Entity-specific port
    networks:
      - genesis-network
    volumes:
      - voi-data:/app/data
    environment:
      - ENTITY_ID=ENT-VOI-APAC-25001
      - DEPLOYMENT_REGION=AWS-ASIA
      - WTO_REGION_BLOCK=APAC
      - DIVINE_ALIGNMENT_ENABLED=true
      - ECG_GOVERNANCE_MODE=active
      - REGIONAL_COMPLIANCE=GST+RBI_EXPORT_REGULATION
      - DIVINE_ALIGNMENT_FACTOR=0.92

  license-api-voi:
    image: genesis-core:latest
    container_name: voi-license-api
    command: python run_license_api.py
    ports:
      - "5101:5001"  # Entity-specific port
    networks:
      - genesis-network
    volumes:
      - voi-data:/app/data
    environment:
      - ENTITY_ID=ENT-VOI-APAC-25001
      - ECG_KEY=${ECG_KEY}
      - HSN_CODE=HSN-GEN-20-03-P
      - LICENSE_TIER=PREMIUM
      - REGION_CODE=REG-APAC
      - LOCAL_CURRENCY=INR
      - REGION_MULTIPLIER=1.35

  license-management-voi:
    image: genesis-core:latest
    container_name: voi-license-management
    command: python run_license_management.py
    ports:
      - "8105:8505"  # Entity-specific port
    networks:
      - genesis-network
    volumes:
      - voi-data:/app/data
    depends_on:
      - license-api-voi
    environment:
      - ENTITY_ID=ENT-VOI-APAC-25001
      - BRAND_IDENTITY=VOI_JEANS
      - IP_REGISTRY_ENABLED=true
      - TRADEMARK_VALIDATION=true

  voi-inventory:
    image: genesis-core:latest
    container_name: voi-inventory-management
    command: streamlit run voi_inventory_management.py --server.port 5150
    ports:
      - "5150:5150"  # Entity-specific port for VSR
    networks:
      - genesis-network
    volumes:
      - voi-data:/app/data
    depends_on:
      - license-api-voi
    environment:
      - ENTITY_ID=ENT-VOI-APAC-25001
      - INVENTORY_SOURCE=SCOTTS_GARMENTS
      - CONNECTION_ID=VOI-SCOTTS-2025-001
      - HSN_CODE=HSN-GEN-60-03-P
      - REGION_SPECIFIC_PRICING=true
      - DIVINE_ALIGNMENT_CHECK=enabled

networks:
  genesis-network:
    driver: bridge

volumes:
  voi-data:
```

### Scotts Garments Container Configuration
```yaml
# docker-compose.scotts-garments.yml
version: '3.8'

services:
  welcome-server-scotts:
    image: genesis-core:latest
    container_name: scotts-welcome-server
    command: python web_server.py
    ports:
      - "8290:8090"  # Entity-specific port
    networks:
      - genesis-network
    volumes:
      - scotts-data:/app/data
    environment:
      - ENTITY_ID=ENT-SCOTTS-APAC-25002
      - DEPLOYMENT_REGION=AWS-ASIA
      - WTO_REGION_BLOCK=SAARC
      - DIVINE_ALIGNMENT_ENABLED=true
      - ECG_GOVERNANCE_MODE=active
      - REGIONAL_COMPLIANCE=BANGLADESH_EXPORT_PROTOCOL
      - DIVINE_ALIGNMENT_FACTOR=0.88

  license-api-scotts:
    image: genesis-core:latest
    container_name: scotts-license-api
    command: python run_license_api.py
    ports:
      - "5201:5001"  # Entity-specific port
    networks:
      - genesis-network
    volumes:
      - scotts-data:/app/data
    environment:
      - ENTITY_ID=ENT-SCOTTS-APAC-25002
      - ECG_KEY=${ECG_KEY}
      - HSN_CODE=HSN-GEN-20-02-S
      - LICENSE_TIER=STANDARD
      - REGION_CODE=REG-SAARC
      - LOCAL_CURRENCY=BDT
      - REGION_MULTIPLIER=1.15

  license-management-scotts:
    image: genesis-core:latest
    container_name: scotts-license-management
    command: python run_license_management.py
    ports:
      - "8205:8505"  # Entity-specific port
    networks:
      - genesis-network
    volumes:
      - scotts-data:/app/data
    depends_on:
      - license-api-scotts
    environment:
      - ENTITY_ID=ENT-SCOTTS-APAC-25002
      - MANUFACTURER_CODE=SG-BD-001
      - COMPLIANCE_AUDIT_LEVEL=STANDARD

  manufacturing-interface:
    image: genesis-core:latest
    container_name: scotts-manufacturing
    command: streamlit run manufacturing_interface.py --server.port 5250
    ports:
      - "5250:5250"  # Entity-specific port for VSR
    networks:
      - genesis-network
    volumes:
      - scotts-data:/app/data
    depends_on:
      - license-api-scotts
    environment:
      - ENTITY_ID=ENT-SCOTTS-APAC-25002
      - PRODUCTION_TRACKING=enabled
      - QUALITY_GOVERNANCE=standard
      - CLIENT_ID=ENT-VOI-APAC-25001
      - HSN_CODE=HSN-GEN-60-02-S
      - REGION_SPECIFIC_COMPLIANCE=true

networks:
  genesis-network:
    driver: bridge

volumes:
  scotts-data:
```

### ECG Governance Container Configuration
```yaml
# docker-compose.ecg-governance.yml
version: '3.8'

services:
  ecg-hsn-registry:
    image: genesis-ecg-hsn:latest
    container_name: ecg-hsn-registry
    ports:
      - "5005:5005"
    networks:
      - genesis-network
    volumes:
      - ecg-data:/app/data/hsn
    environment:
      - ECG_KEY=${ECG_KEY}
      - HSN_REGISTRY_MODE=active
      - LICENSE_VALIDATION_ENABLED=true
      - DIVINE_ALIGNMENT_CHECK=enabled
      - MASTER_GOVERNANCE=true
      - WTO_COMPLIANCE_REGISTRY=/app/data/hsn/wto_compliance_registry.json

  ecg-governance-dashboard:
    image: genesis-ecg-dashboard:latest
    container_name: ecg-governance-dashboard
    command: streamlit run empire_os_dashboard.py --server.port 5000
    ports:
      - "5000:5000"
    networks:
      - genesis-network
    volumes:
      - ecg-data:/app/data
    environment:
      - ECG_KEY=${ECG_KEY}
      - EMPEROR_ACCESS=true
      - GOVERNANCE_VIEW=global
      - ENTITIES_MONITORED=ENT-VOI-APAC-25001,ENT-SCOTTS-APAC-25002
      - DIVINE_ALIGNMENT_TRACKING=enabled
      - DAY7_READINESS_MONITOR=active

  npu-coordinator:
    image: genesis-npu:latest
    container_name: ecg-npu-coordinator
    command: python tools/run_npu_coordinator.py
    networks:
      - genesis-network
    volumes:
      - ecg-data:/app/data
    environment:
      - ECG_KEY=${ECG_KEY}
      - NPU_MODE=coordinator
      - ASSIGNED_ENTITIES=ENT-VOI-APAC-25001,ENT-SCOTTS-APAC-25002
      - DIVINE_ALIGNMENT_PRIORITY=maximum
      - CONVERGENCE_MONITOR=active

networks:
  genesis-network:
    driver: bridge

volumes:
  ecg-data:
```

## 3. HSN License Manifest Configuration

### Voi Jeans HSN License Manifest
```json
{
  "manifest_id": "GEN-MANIFEST-VOI-001",
  "client_id": "ENT-VOI-APAC-25001",
  "deployment_id": "VOI-DEPLOY-25001",
  "license_key": "SYN-VOI-APAC-2025-PREM",
  "issue_date": "2025-01-01",
  "expiration_date": "2026-01-01",
  "wto_region": {
    "region_block": "APAC",
    "country": "India",
    "wto_compliance": "Developing Economy Protocol",
    "jurisdiction_rules": "GST + RBI Export Regulation",
    "divine_alignment_factor": 0.92,
    "region_code": "REG-APAC"
  },
  "components": [
    {
      "hsn_code": "HSN-GEN-10-03-P",
      "component_name": "Core Infrastructure",
      "tier": "Premium",
      "quantity": 1,
      "base_price": 1.50,
      "user_count": 250,
      "user_scaling_price": 0.0075,
      "npu_count": 3,
      "npu_scaling_price": 0.36,
      "region": "AWS-ASIA",
      "region_multiplier": 1.35,
      "duration": "annual",
      "duration_multiplier": 10.0,
      "total_component_price": 25.22625,
      "local_currency_code": "INR",
      "local_pricing": true
    },
    {
      "hsn_code": "HSN-GEN-20-03-P",
      "component_name": "License Services",
      "tier": "Premium",
      "quantity": 1,
      "base_price": 1.25,
      "user_count": 250,
      "user_scaling_price": 0.0075,
      "npu_count": 3,
      "npu_scaling_price": 0.3,
      "region": "AWS-ASIA",
      "region_multiplier": 1.35,
      "duration": "annual",
      "duration_multiplier": 10.0,
      "total_component_price": 21.76625,
      "local_currency_code": "INR",
      "local_pricing": true
    },
    {
      "hsn_code": "HSN-GEN-30-03-P",
      "component_name": "Entity Services",
      "tier": "Premium",
      "quantity": 5,
      "base_price": 0.85,
      "user_count": 250,
      "user_scaling_price": 0.01,
      "npu_count": 3,
      "npu_scaling_price": 0.24,
      "region": "AWS-ASIA",
      "region_multiplier": 1.35,
      "duration": "annual",
      "duration_multiplier": 10.0,
      "total_component_price": 69.525,
      "local_currency_code": "INR",
      "local_pricing": true
    },
    {
      "hsn_code": "HSN-GEN-40-03-P",
      "component_name": "NPU Services",
      "tier": "Premium - Cluster",
      "quantity": 1,
      "base_price": 1.50,
      "user_count": 250,
      "user_scaling_price": 0.0075,
      "npu_count": 3,
      "npu_scaling_price": 0.0,
      "region": "AWS-ASIA",
      "region_multiplier": 1.35,
      "duration": "annual",
      "duration_multiplier": 10.0,
      "total_component_price": 20.25,
      "local_currency_code": "INR",
      "local_pricing": true
    },
    {
      "hsn_code": "HSN-GEN-50-03-P",
      "component_name": "Divine Alignment",
      "tier": "Premium",
      "quantity": 1,
      "base_price": 1.10,
      "user_count": 250,
      "user_scaling_price": 0.0075,
      "npu_count": 3,
      "npu_scaling_price": 0.3,
      "region": "AWS-ASIA",
      "region_multiplier": 1.35,
      "duration": "annual",
      "duration_multiplier": 10.0,
      "total_component_price": 19.845,
      "local_currency_code": "INR",
      "local_pricing": true
    },
    {
      "hsn_code": "HSN-GEN-60-03-P",
      "component_name": "Virtual Silk Road",
      "tier": "Premium",
      "quantity": 1,
      "base_price": 2.00,
      "user_count": 250,
      "user_scaling_price": 0.01,
      "npu_count": 3,
      "npu_scaling_price": 0.36,
      "region": "AWS-ASIA",
      "region_multiplier": 1.35,
      "duration": "annual",
      "duration_multiplier": 10.0,
      "total_component_price": 31.995,
      "local_currency_code": "INR",
      "local_pricing": true
    }
  ],
  "subtotal": 188.60875,
  "volume_discount_rate": 0.05,
  "volume_discount_amount": 9.430437,
  "regional_compliance_discount": 0.07,
  "regional_compliance_amount": 13.202612,
  "total_price": 165.9757,
  "currency": "BTC",
  "local_currency_total": "₹14,108,299",
  "payment_terms": "Net 30",
  "divine_alignment_factor": 0.92,
  "amendments": [
    {
      "amendment_id": "GEN-AMD-VOI-2025-01",
      "date": "2025-04-01",
      "reason": "WTO Region Update - India TPR 2025",
      "changes": [
        {
          "field": "tax_policy",
          "old": "Flat GST 18%",
          "new": "Variable GST slab with digital exports at 0%"
        },
        {
          "field": "divine_alignment_factor",
          "old": 0.90,
          "new": 0.92
        }
      ],
      "impact": "Reduced license cost by 7%"
    }
  ]
}
```

### Scotts Garments HSN License Manifest
```json
{
  "manifest_id": "GEN-MANIFEST-SCOTTS-001",
  "client_id": "ENT-SCOTTS-APAC-25002",
  "deployment_id": "SCOTTS-DEPLOY-25001",
  "license_key": "SYN-SCOTTS-SAARC-2025-STD",
  "issue_date": "2025-01-10",
  "expiration_date": "2026-01-10",
  "wto_region": {
    "region_block": "SAARC",
    "country": "Bangladesh",
    "wto_compliance": "Least Developed Country Protocol",
    "jurisdiction_rules": "Bangladesh Export Protocol",
    "divine_alignment_factor": 0.88,
    "region_code": "REG-SAARC"
  },
  "components": [
    {
      "hsn_code": "HSN-GEN-10-02-S",
      "component_name": "Core Infrastructure",
      "tier": "Standard",
      "quantity": 1,
      "base_price": 0.75,
      "user_count": 100,
      "user_scaling_price": 0.002,
      "npu_count": 2,
      "npu_scaling_price": 0.16,
      "region": "AWS-ASIA",
      "region_multiplier": 1.15,
      "duration": "annual",
      "duration_multiplier": 10.0,
      "total_component_price": 10.925,
      "local_currency_code": "BDT",
      "local_pricing": true
    },
    {
      "hsn_code": "HSN-GEN-20-02-S",
      "component_name": "License Services",
      "tier": "Standard",
      "quantity": 1,
      "base_price": 0.50,
      "user_count": 100,
      "user_scaling_price": 0.002,
      "npu_count": 2,
      "npu_scaling_price": 0.10,
      "region": "AWS-ASIA",
      "region_multiplier": 1.15,
      "duration": "annual",
      "duration_multiplier": 10.0,
      "total_component_price": 7.475,
      "local_currency_code": "BDT",
      "local_pricing": true
    },
    {
      "hsn_code": "HSN-GEN-30-02-S",
      "component_name": "Entity Services",
      "tier": "Standard",
      "quantity": 3,
      "base_price": 0.35,
      "user_count": 100,
      "user_scaling_price": 0.003,
      "npu_count": 2,
      "npu_scaling_price": 0.08,
      "region": "AWS-ASIA",
      "region_multiplier": 1.15,
      "duration": "annual",
      "duration_multiplier": 10.0,
      "total_component_price": 15.18,
      "local_currency_code": "BDT",
      "local_pricing": true
    },
    {
      "hsn_code": "HSN-GEN-40-02-S",
      "component_name": "NPU Services",
      "tier": "Standard - Dedicated",
      "quantity": 2,
      "base_price": 0.60,
      "user_count": 100,
      "user_scaling_price": 0.002,
      "npu_count": 2,
      "npu_scaling_price": 0.0,
      "region": "AWS-ASIA",
      "region_multiplier": 1.15,
      "duration": "annual",
      "duration_multiplier": 10.0,
      "total_component_price": 14.26,
      "local_currency_code": "BDT",
      "local_pricing": true
    },
    {
      "hsn_code": "HSN-GEN-60-02-S",
      "component_name": "Virtual Silk Road",
      "tier": "Standard",
      "quantity": 1,
      "base_price": 0.80,
      "user_count": 100,
      "user_scaling_price": 0.003,
      "npu_count": 2,
      "npu_scaling_price": 0.16,
      "region": "AWS-ASIA",
      "region_multiplier": 1.15,
      "duration": "annual",
      "duration_multiplier": 10.0,
      "total_component_price": 11.27,
      "local_currency_code": "BDT",
      "local_pricing": true
    }
  ],
  "subtotal": 59.11,
  "volume_discount_rate": 0.05,
  "volume_discount_amount": 2.9555,
  "regional_compliance_discount": 0.15,
  "regional_compliance_amount": 8.8665,
  "total_price": 47.288,
  "currency": "BTC",
  "local_currency_total": "৳5,910,820",
  "payment_terms": "Net 30",
  "divine_alignment_factor": 0.88,
  "amendments": [
    {
      "amendment_id": "GEN-AMD-SCOTTS-2025-01",
      "date": "2025-03-15",
      "reason": "WTO Region Update - LDC Preferential Treatment",
      "changes": [
        {
          "field": "regional_compliance_discount",
          "old": 0.10,
          "new": 0.15
        },
        {
          "field": "divine_alignment_factor",
          "old": 0.85,
          "new": 0.88
        }
      ],
      "impact": "Reduced license cost by 15%"
    }
  ]
}
```

## 4. Trade Relationship Configuration

### Voi Jeans to Scotts Garments Trade Relationship
```json
{
  "relationship_id": "REL-VOI-SCOTTS-25001",
  "source_entity_id": "ENT-VOI-APAC-25001",
  "target_entity_id": "ENT-SCOTTS-APAC-25002",
  "relationship_type": "BRAND_OWNER_TO_MANUFACTURER",
  "contract_id": "VOI-SCOTTS-2025-001",
  "initialized_date": "2025-01-15",
  "status": "ACTIVE",
  "trade_terms": {
    "currency": "USD",
    "payment_terms": "Net 45",
    "minimum_order_value": 50000,
    "delivery_terms": "FOB Chittagong",
    "quality_standards": ["ISO 9001", "OEKO-TEX Standard 100"],
    "compliance_requirements": ["BSCI", "WRAP", "Fair Trade"]
  },
  "wto_compliance": {
    "rules_of_origin": "SAFTA Rules of Origin",
    "tariff_classification": "HS Chapter 61-62",
    "preferential_treatment": "SAFTA LDC Treatment",
    "documentation_requirements": [
      "Certificate of Origin Form SAFTA",
      "Commercial Invoice",
      "Packing List",
      "Bill of Lading"
    ]
  },
  "governance_parameters": {
    "divine_alignment_requirement": 0.85,
    "quality_inspection_frequency": "Every Lot",
    "compliance_audit_frequency": "Quarterly",
    "license_verification_frequency": "Monthly"
  }
}
```

## 5. Divine Alignment Configuration

### Voi Jeans Divine Alignment
```json
{
  "entity_id": "ENT-VOI-APAC-25001",
  "divine_alignment_factor": 0.92,
  "divine_alignment_components": {
    "ethical_sourcing": 0.94,
    "environmental_sustainability": 0.91,
    "labor_practices": 0.93,
    "governance_transparency": 0.90,
    "community_engagement": 0.92
  },
  "alignment_audit_schedule": "Quarterly",
  "alignment_targets": {
    "current": 0.92,
    "target_2025_q4": 0.94,
    "target_2026_q2": 0.95,
    "day7_readiness_target": 0.98
  },
  "divine_convergence_preparation": {
    "status": "IN_PROGRESS",
    "completion_percentage": 68,
    "next_milestone": "Ethical Sourcing Enhancement",
    "milestone_deadline": "2025-06-30"
  }
}
```

### Scotts Garments Divine Alignment
```json
{
  "entity_id": "ENT-SCOTTS-APAC-25002",
  "divine_alignment_factor": 0.88,
  "divine_alignment_components": {
    "ethical_sourcing": 0.86,
    "environmental_sustainability": 0.85,
    "labor_practices": 0.91,
    "governance_transparency": 0.89,
    "community_engagement": 0.89
  },
  "alignment_audit_schedule": "Quarterly",
  "alignment_targets": {
    "current": 0.88,
    "target_2025_q4": 0.90,
    "target_2026_q2": 0.92,
    "day7_readiness_target": 0.95
  },
  "divine_convergence_preparation": {
    "status": "IN_PROGRESS",
    "completion_percentage": 55,
    "next_milestone": "Environmental Sustainability Initiative",
    "milestone_deadline": "2025-09-30"
  }
}
```

## 6. Docker Deployment Commands

### For Initial Deployment

```bash
# Set up environment variables
export ECG_KEY=emperorkey123
export VOI_REPO_PATH=/path/to/voi/source
export SCOTTS_REPO_PATH=/path/to/scotts/source
export ECG_REPO_PATH=/path/to/ecg/source

# Build the Docker images
docker build -t genesis-core:latest -f ${ECG_REPO_PATH}/Core.Dockerfile ${ECG_REPO_PATH}
docker build -t genesis-ecg-hsn:latest -f ${ECG_REPO_PATH}/ECG-HSN.Dockerfile ${ECG_REPO_PATH}
docker build -t genesis-ecg-dashboard:latest -f ${ECG_REPO_PATH}/ECG-Dashboard.Dockerfile ${ECG_REPO_PATH}
docker build -t genesis-npu:latest -f ${ECG_REPO_PATH}/NPU.Dockerfile ${ECG_REPO_PATH}

# Deploy ECG Governance containers
docker-compose -f ${ECG_REPO_PATH}/docker-compose.ecg-governance.yml up -d

# Deploy Voi Jeans containers
docker-compose -f ${VOI_REPO_PATH}/docker-compose.voi-jeans.yml up -d

# Deploy Scotts Garments containers
docker-compose -f ${SCOTTS_REPO_PATH}/docker-compose.scotts-garments.yml up -d

# Verify deployments
docker-compose -f ${ECG_REPO_PATH}/docker-compose.ecg-governance.yml ps
docker-compose -f ${VOI_REPO_PATH}/docker-compose.voi-jeans.yml ps
docker-compose -f ${SCOTTS_REPO_PATH}/docker-compose.scotts-garments.yml ps
```

### For License Verification

```bash
# Verify Voi Jeans license
docker-compose exec ecg-hsn-registry python tools/verify_license.py \
  --entity ENT-VOI-APAC-25001 \
  --license-key SYN-VOI-APAC-2025-PREM

# Verify Scotts Garments license
docker-compose exec ecg-hsn-registry python tools/verify_license.py \
  --entity ENT-SCOTTS-APAC-25002 \
  --license-key SYN-SCOTTS-SAARC-2025-STD

# Verify trade relationship
docker-compose exec ecg-hsn-registry python tools/verify_relationship.py \
  --source ENT-VOI-APAC-25001 \
  --target ENT-SCOTTS-APAC-25002 \
  --relationship-id REL-VOI-SCOTTS-25001
```

## 7. Access Points

### Voi Jeans Access URLs
- **Welcome Server**: http://[host-ip]:8190/
- **License API**: http://[host-ip]:5101/
- **License Management**: http://[host-ip]:8105/
- **Inventory Management**: http://[host-ip]:5150/

### Scotts Garments Access URLs
- **Welcome Server**: http://[host-ip]:8290/
- **License API**: http://[host-ip]:5201/
- **License Management**: http://[host-ip]:8205/
- **Manufacturing Interface**: http://[host-ip]:5250/

### ECG Governance Access URLs
- **HSN Registry API**: http://[host-ip]:5005/
- **Governance Dashboard**: http://[host-ip]:5000/

## 8. WTO Compliance Summary

### Voi Jeans (India) - APAC Region
- **Compliance Protocol**: Developing Economy Protocol
- **Regional Rules**: GST + RBI Export Regulation
- **Divine Alignment Factor**: 0.92
- **Tariff Benefits**: Variable GST slab with digital exports at 0%
- **Regional Compliance Discount**: 7%
- **Regional Trade Framework**: Pan-Asia Trade Framework

### Scotts Garments (Bangladesh) - SAARC Region
- **Compliance Protocol**: Least Developed Country Protocol
- **Regional Rules**: Bangladesh Export Protocol
- **Divine Alignment Factor**: 0.88
- **Tariff Benefits**: LDC Preferential Treatment
- **Regional Compliance Discount**: 15%
- **Regional Trade Framework**: South Asian Preferential Trading Arrangement

### Trade Relationship Compliance
- **Rules of Origin**: SAFTA Rules of Origin
- **Tariff Classification**: HS Chapter 61-62
- **Preferential Treatment**: SAFTA LDC Treatment
- **Required Documentation**: Certificate of Origin Form SAFTA

---

*Issued under the authority of the Emperor's Computational Governance.*

*Built with divine mechanics. Deployed with sovereign integrity. Governed by computational alignment.*