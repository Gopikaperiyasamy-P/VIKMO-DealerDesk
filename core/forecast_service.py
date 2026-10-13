import csv
import math
import os
import statistics
from django.conf import settings
from core.models import Product
from core.exceptions import CustomAPIException

# Cached data structures
_FORECAST_DATA = None
_LEAD_TIMES = None
_SIGMAS = None


def load_forecast_metadata():
    global _FORECAST_DATA, _LEAD_TIMES, _SIGMAS
    if _FORECAST_DATA is not None:
        return _FORECAST_DATA, _LEAD_TIMES, _SIGMAS

    repo_dir = settings.BASE_DIR
    forecast_path = repo_dir / "ml" / "forecast.csv"
    lead_path = repo_dir / "data" / "lead_times.csv"
    sales_path = repo_dir / "data" / "sales_history.csv"

    # 1. Load lead times
    lead_times = {}
    if lead_path.exists():
        with open(lead_path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                lead_times[r["sku"].strip()] = int(r["lead_time_weeks"].strip())

    # 2. Load forecast.csv
    forecast_data = {}
    if forecast_path.exists():
        with open(forecast_path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                sku = r["sku"].strip()
                if sku not in forecast_data:
                    forecast_data[sku] = []
                forecast_data[sku].append({
                    "week_start": r["week_start"].strip(),
                    "forecast_units": float(r["forecast_units"].strip())
                })
        # sort each sku's forecast chronologically
        for sku in forecast_data:
            forecast_data[sku] = sorted(forecast_data[sku], key=lambda x: x["week_start"])

    # 3. Compute sigma (sample standard deviation of most recent 12 weeks of sales_history)
    sigmas = {}
    if sales_path.exists():
        sku_sales = {}
        with open(sales_path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                sku = r["sku"].strip()
                if sku not in sku_sales:
                    sku_sales[sku] = []
                sku_sales[sku].append((r["week_start"].strip(), float(r["units_sold"].strip())))
        
        for sku, items in sku_sales.items():
            # sort chronologically and take last 12 weeks
            items = sorted(items, key=lambda x: x[0])
            last12 = [x[1] for x in items[-12:]]
            if len(last12) >= 2:
                sigmas[sku] = statistics.stdev(last12)
            elif len(last12) == 1:
                sigmas[sku] = 0.0
            else:
                sigmas[sku] = 0.0

    _FORECAST_DATA = forecast_data
    _LEAD_TIMES = lead_times
    _SIGMAS = sigmas
    return _FORECAST_DATA, _LEAD_TIMES, _SIGMAS


def get_sku_forecast(sku: str):
    forecast_data, lead_times, _ = load_forecast_metadata()
    if sku not in lead_times or sku not in forecast_data:
        raise CustomAPIException(
            code="NOT_FOUND",
            message=f"No forecast found for SKU {sku}",
            details=[f"SKU {sku} is not in the forecast portfolio"],
            status_code=404,
        )
    return {
        "sku": sku,
        "forecast": forecast_data[sku],
    }


def get_reorder_suggestions():
    forecast_data, lead_times, sigmas = load_forecast_metadata()
    all_skus = list(lead_times.keys())

    # Fetch live stock from DB
    db_products = {p.sku: p.stock for p in Product.objects.filter(sku__in=all_skus)}

    results = []
    for sku in all_skus:
        L = lead_times[sku]
        sku_forecast = forecast_data.get(sku, [])
        first_L_weeks = sku_forecast[:L]
        lead_time_demand = round(sum(w["forecast_units"] for w in first_L_weeks), 1)

        sigma = sigmas.get(sku, 0.0)
        safety_stock = math.ceil(1.65 * sigma * math.sqrt(L))
        reorder_point = round(lead_time_demand + safety_stock, 1)

        current_stock = db_products.get(sku, 0)
        reorder_qty = max(0, math.ceil(reorder_point - current_stock))

        results.append({
            "sku": sku,
            "current_stock": current_stock,
            "lead_time_weeks": L,
            "lead_time_demand": lead_time_demand,
            "safety_stock": safety_stock,
            "reorder_point": reorder_point,
            "reorder_qty": reorder_qty,
        })

    return {"results": results}
