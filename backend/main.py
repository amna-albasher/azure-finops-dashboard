from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import random
import math

app = FastAPI(title="Azure FinOps Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed for consistent mock data
random.seed(42)

def generate_daily_spend(days=30, base=1200, variance=300):
    """Generate realistic daily spend with weekday/weekend patterns"""
    spend = []
    today = datetime.now()
    for i in range(days, 0, -1):
        date = today - timedelta(days=i)
        # Lower spend on weekends
        weekend_factor = 0.65 if date.weekday() >= 5 else 1.0
        # Slight upward trend over time
        trend = 1 + (days - i) * 0.003
        # Random variance
        noise = random.uniform(-variance, variance)
        amount = round((base * weekend_factor * trend) + noise, 2)
        spend.append({
            "date": date.strftime("%b %d"),
            "amount": max(amount, 200),
            "forecast": None
        })
    # Add 7 day forecast
    last_avg = sum(d["amount"] for d in spend[-7:]) / 7
    for i in range(1, 8):
        date = today + timedelta(days=i)
        forecast = round(last_avg * (1 + i * 0.005) + random.uniform(-100, 100), 2)
        spend.append({
            "date": date.strftime("%b %d"),
            "amount": None,
            "forecast": forecast
        })
    return spend

RESOURCE_GROUPS = [
    {"name": "rg-production-uae-north", "env": "Production", "spend": 18420.50, "budget": 20000, "resources": 47},
    {"name": "rg-staging-uae-north", "env": "Staging", "spend": 6830.20, "budget": 8000, "resources": 23},
    {"name": "rg-development-uae-north", "env": "Development", "spend": 3210.80, "budget": 5000, "resources": 31},
    {"name": "rg-shared-services", "env": "Shared", "spend": 4890.40, "budget": 5500, "resources": 18},
    {"name": "rg-data-analytics", "env": "Production", "spend": 7640.10, "budget": 7000, "resources": 12},
]

TOP_RESOURCES = [
    {"name": "aks-prod-cluster-01", "type": "Azure Kubernetes Service", "rg": "rg-production-uae-north", "daily": 187.40, "monthly": 5622.00, "trend": +8.2},
    {"name": "vm-sql-primary-prod", "type": "Virtual Machine (D8s v3)", "rg": "rg-production-uae-north", "daily": 98.20, "monthly": 2946.00, "trend": +1.1},
    {"name": "databricks-analytics-ws", "type": "Azure Databricks", "rg": "rg-data-analytics", "daily": 84.60, "monthly": 2538.00, "trend": +15.4},
    {"name": "apim-gateway-prod", "type": "API Management (Premium)", "rg": "rg-production-uae-north", "daily": 76.30, "monthly": 2289.00, "trend": -2.3},
    {"name": "storage-backup-lrs-001", "type": "Storage Account (LRS)", "rg": "rg-shared-services", "daily": 54.10, "monthly": 1623.00, "trend": +4.7},
    {"name": "vnet-hub-prod-uae", "type": "VPN Gateway (VpnGw2)", "rg": "rg-shared-services", "daily": 48.90, "monthly": 1467.00, "trend": 0.0},
    {"name": "acr-prod-registry", "type": "Container Registry (Premium)", "rg": "rg-production-uae-north", "daily": 41.20, "monthly": 1236.00, "trend": +2.8},
    {"name": "redis-cache-prod-01", "type": "Azure Cache for Redis (P2)", "rg": "rg-production-uae-north", "daily": 38.70, "monthly": 1161.00, "trend": -1.2},
]

WASTE_ALERTS = [
    {
        "id": "W001",
        "severity": "high",
        "resource": "vm-dev-test-07",
        "type": "Virtual Machine",
        "rg": "rg-development-uae-north",
        "issue": "VM running at <3% CPU for 28 days",
        "estimated_waste": 412.80,
        "recommendation": "Downsize to B2s or deallocate when not in use",
        "days_detected": 28
    },
    {
        "id": "W002",
        "severity": "high",
        "resource": "disk-orphaned-prod-backup",
        "type": "Managed Disk (Premium SSD 1TB)",
        "rg": "rg-production-uae-north",
        "issue": "Unattached disk with no VM association",
        "estimated_waste": 138.24,
        "recommendation": "Snapshot and delete or attach to active VM",
        "days_detected": 45
    },
    {
        "id": "W003",
        "severity": "medium",
        "resource": "pip-staging-lb-unused",
        "type": "Public IP Address",
        "rg": "rg-staging-uae-north",
        "issue": "Static IP unassociated for 60+ days",
        "estimated_waste": 26.28,
        "recommendation": "Release IP or associate with a resource",
        "days_detected": 63
    },
    {
        "id": "W004",
        "severity": "medium",
        "resource": "aks-dev-nodepool-gpu",
        "type": "AKS Node Pool (NC6s v3)",
        "rg": "rg-development-uae-north",
        "issue": "GPU node pool idle, no workloads scheduled",
        "estimated_waste": 892.40,
        "recommendation": "Scale to 0 nodes or delete node pool",
        "days_detected": 14
    },
    {
        "id": "W005",
        "severity": "low",
        "resource": "snapshot-db-2024-01-*",
        "type": "Disk Snapshots (12 items)",
        "rg": "rg-shared-services",
        "issue": "Snapshots older than 90 days with no retention policy",
        "estimated_waste": 67.20,
        "recommendation": "Apply retention policy and delete expired snapshots",
        "days_detected": 90
    },
]

SERVICE_BREAKDOWN = [
    {"service": "Compute", "amount": 16840.20, "percentage": 41.2},
    {"service": "Kubernetes", "amount": 8920.50, "percentage": 21.8},
    {"service": "Storage", "amount": 5430.10, "percentage": 13.3},
    {"service": "Networking", "amount": 4210.80, "percentage": 10.3},
    {"service": "Databases", "amount": 3180.40, "percentage": 7.8},
    {"service": "AI & Analytics", "amount": 2320.00, "percentage": 5.7},
]

@app.get("/")
def root():
    return {"status": "Azure FinOps Dashboard API", "version": "1.0.0"}

@app.get("/api/overview")
def get_overview():
    total_spend = 40992.00
    budget = 45000.00
    last_month = 37840.50
    daily_avg = round(total_spend / 22, 2)  # 22 working days
    forecast = round(daily_avg * 30, 2)
    waste_total = sum(w["estimated_waste"] for w in WASTE_ALERTS)

    return {
        "period": "July 2026",
        "total_spend": total_spend,
        "budget": budget,
        "budget_used_pct": round((total_spend / budget) * 100, 1),
        "remaining_budget": round(budget - total_spend, 2),
        "last_month_spend": last_month,
        "mom_change_pct": round(((total_spend - last_month) / last_month) * 100, 1),
        "daily_average": daily_avg,
        "forecast_month_end": forecast,
        "waste_identified": round(waste_total, 2),
        "waste_alerts_count": len(WASTE_ALERTS),
        "resources_monitored": sum(rg["resources"] for rg in RESOURCE_GROUPS),
        "subscriptions": 1,
        "resource_groups": len(RESOURCE_GROUPS),
        "last_updated": datetime.now().strftime("%d %b %Y, %H:%M UTC")
    }

@app.get("/api/daily-spend")
def get_daily_spend():
    return {"data": generate_daily_spend()}

@app.get("/api/resource-groups")
def get_resource_groups():
    rgs = []
    for rg in RESOURCE_GROUPS:
        pct = round((rg["spend"] / rg["budget"]) * 100, 1)
        status = "critical" if pct > 95 else "warning" if pct > 80 else "healthy"
        rgs.append({**rg, "budget_used_pct": pct, "status": status})
    return {"data": rgs}

@app.get("/api/top-resources")
def get_top_resources():
    return {"data": TOP_RESOURCES}

@app.get("/api/waste-alerts")
def get_waste_alerts():
    total_waste = sum(w["estimated_waste"] for w in WASTE_ALERTS)
    return {
        "total_waste": round(total_waste, 2),
        "count": len(WASTE_ALERTS),
        "data": WASTE_ALERTS
    }

@app.get("/api/service-breakdown")
def get_service_breakdown():
    return {"data": SERVICE_BREAKDOWN}
