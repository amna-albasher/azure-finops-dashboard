# Azure FinOps Dashboard

> Real-time Azure cost intelligence dashboard — tracks spend, detects waste, and forecasts cloud costs across environments.

**Live Demo:** [finops-dashboard.vercel.app](https://finops-dashboard.vercel.app)  
**API:** [azure-finops-api.vercel.app](https://azure-finops-api.vercel.app)

---

## What It Does

- **Cost Overview** — Month-to-date spend, budget utilization, and month-end forecast
- **Daily Spend Chart** — 30-day history with 7-day AI forecast
- **Resource Group Breakdown** — Budget utilization per environment (prod/staging/dev)
- **Top Resources by Cost** — Ranked table with spend trends
- **Waste Detection** — Identifies idle VMs, orphaned disks, unattached IPs
- **Service Breakdown** — Cost distribution across Azure service categories

## Problem It Solves

Cloud bills arrive at month-end with no visibility into what's driving cost. This dashboard gives engineering and finance teams **live cost intelligence** — so waste is caught early, budgets are tracked daily, and no one gets surprised.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Frontend | HTML, CSS, Chart.js |
| Data | Azure Cost Management API (mock for demo) |
| Deployment | Vercel |
| CI/CD | GitHub Actions |

## Project Structure

```
finops-dashboard/
├── backend/
│   ├── main.py          # FastAPI API with mock Azure cost data
│   ├── requirements.txt
│   └── vercel.json
├── frontend/
│   ├── index.html       # Full dashboard UI
│   └── vercel.json
└── README.md
```

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API available at: `http://localhost:8000`  
Docs at: `http://localhost:8000/docs`

### Frontend
```bash
cd frontend
# Open index.html in browser or use live server
npx serve .
```

## Deploy to Vercel

### Backend (API)
```bash
cd backend
vercel --prod
# Note the URL e.g. https://azure-finops-api.vercel.app
```

### Frontend
```bash
cd frontend
# Update API URL in index.html if connecting to real API
vercel --prod
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/overview` | KPI summary — total spend, budget, forecast, waste |
| `GET /api/daily-spend` | 30-day spend history + 7-day forecast |
| `GET /api/resource-groups` | Budget utilization per resource group |
| `GET /api/top-resources` | Top 8 resources by monthly cost |
| `GET /api/waste-alerts` | Identified waste with recommendations |
| `GET /api/service-breakdown` | Cost split by Azure service type |

## Connecting to Real Azure Data

Replace mock data with Azure Cost Management API:

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient

credential = DefaultAzureCredential()
client = CostManagementClient(credential)
```

Required permissions: `Cost Management Reader` role on subscription.

## Author

**Amna Albasher** — Cloud & DevOps Engineer  
[LinkedIn](https://linkedin.com/in/amna-albasher) · [GitHub](https://github.com/amna-albasher) · [Portfolio](https://amna-albasher.github.io/amna-portfolio)
