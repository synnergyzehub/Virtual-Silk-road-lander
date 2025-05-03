
# Genesis Stack – Deployment Guide

This document outlines how to install, configure, and launch the Genesis backend and UI components.

---

## Backend Setup (Ubuntu)

### Prerequisites:
- Ubuntu 20.04+
- sudo access
- Internet connectivity

### Step-by-step:

1. **Download and Run Deployment Script**
```bash
chmod +x genesis_deploy_ubuntu.sh
./genesis_deploy_ubuntu.sh
```

2. **API Runs At**
```
http://localhost:5000/
```

3. **Docker Services**
- MySQL + Genesis DB auto-initialized
- Config: `genesis_mysql_docker_compose.yml`

4. **Main API File**
- `genesis_api.py` — endpoints for:
  - /digitalme/ledger
  - /license/reputation
  - /vision_logger
  - /digitalme/persona

---

## UI Setup

1. Place all React files in your `/components/ui/` directory.
2. Entry file: `founder_console.jsx`
3. Make sure you have:
```bash
npm install react tailwindcss shadcn/ui
```

4. Start your React app:
```bash
npm run dev
```

---

## Optional Features

- **ECG Notifier**: Console simulation for license risk alert
- **Genesis Vision Logger**: Displays brand journey through 7 Genesis Ages
- **Persona Panel**: Maps traits, sessions, and Genesis alignment

---

## Notes
- Genesis core respects jurisdiction, law, and ethics.
- All actions are logged under DigitalMe with hash-based immutability.
- Recommended to audit every 180 days using revalidation loop.

---

Built with truth. Deployed in clarity. Governed by alignment.
