import os
import csv
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

def generate():
    sales = pd.read_csv('data/sales_history.csv')
    sales['week_start'] = pd.to_datetime(sales['week_start'])
    
    promo = pd.read_csv('data/promo_calendar.csv')
    promo['week_start'] = pd.to_datetime(promo['week_start'])
    
    lead = pd.read_csv('data/lead_times.csv')
    all_skus = sorted(lead['sku'].tolist())
    
    fest = pd.read_csv('data/festival_calendar.csv')
    fest['date'] = pd.to_datetime(fest['date'])
    diwali_dates = fest[fest['festival'] == 'Diwali']['date'].values

    def get_diwali_distance(week_date):
        min_dist_days = 9999
        best_diff_weeks = 0
        for d in diwali_dates:
            diff_days = (pd.to_datetime(week_date) - pd.to_datetime(d)).days
            if abs(diff_days) < abs(min_dist_days):
                min_dist_days = diff_days
                best_diff_weeks = diff_days / 7.0
        return best_diff_weeks

    sku_dummies = {s: i for i, s in enumerate(all_skus)}
    
    # Train features
    features = []
    targets = []
    for sku in all_skus:
        sub = sales[sales['sku'] == sku].sort_values('week_start').reset_index(drop=True)
        if len(sub) < 6:
            continue
        for i in range(12, len(sub)):
            w = sub.loc[i, 'week_start']
            diwali_diff = get_diwali_distance(w)
            f = [
                sub.loc[i-4, 'units_sold'],
                sub.loc[i-5, 'units_sold'],
                sub.loc[i-6, 'units_sold'],
                sub.loc[i-12:i-4, 'units_sold'].mean(),
                sub.loc[i-8:i-4, 'units_sold'].mean(),
                sub.loc[i, 'promo_flag'],
                diwali_diff,
                np.exp(-0.5 * (diwali_diff / 2.0)**2),
                w.month,
                sku_dummies[sku],
            ]
            features.append(f)
            targets.append(sub.loc[i, 'units_sold'])

    reg = GradientBoostingRegressor(n_estimators=75, max_depth=4, learning_rate=0.08, random_state=42)
    reg.fit(features, targets)

    forecast_weeks = ['2026-09-28', '2026-10-05', '2026-10-12', '2026-10-19']
    
    rows = []
    for sku in all_skus:
        sub = sales[sales['sku'] == sku].sort_values('week_start').reset_index(drop=True)
        is_new_sku = len(sub) < 10
        recent_mean = sub['units_sold'].mean() if is_new_sku else sub['units_sold'].tail(12).mean()

        for w_str in forecast_weeks:
            w = pd.to_datetime(w_str)
            p_flag = 0
            pmatch = promo[(promo['sku'] == sku) & (promo['week_start'] == w)]
            if len(pmatch) > 0:
                p_flag = int(pmatch['promo_flag'].iloc[0])

            if is_new_sku:
                # For newly launched SKU with only 6 weeks of data, apply recent mean with promo lift
                pred = recent_mean * (1.35 if p_flag else 1.0)
            else:
                diwali_diff = get_diwali_distance(w)
                f = [[
                    sub['units_sold'].iloc[-1],
                    sub['units_sold'].iloc[-2] if len(sub) > 1 else sub['units_sold'].iloc[-1],
                    sub['units_sold'].iloc[-3] if len(sub) > 2 else sub['units_sold'].iloc[-1],
                    sub['units_sold'].tail(8).mean(),
                    sub['units_sold'].tail(4).mean(),
                    p_flag,
                    diwali_diff,
                    np.exp(-0.5 * (diwali_diff / 2.0)**2),
                    w.month,
                    sku_dummies[sku],
                ]]
                raw_pred = float(reg.predict(f)[0])
                pred = max(0.0, raw_pred)

            rows.append({
                'sku': sku,
                'week_start': w_str,
                'forecast_units': round(float(pred), 1)
            })

    # Sort rows by sku and week_start
    rows = sorted(rows, key=lambda x: (x['sku'], x['week_start']))
    
    out_path = os.path.join('ml', 'forecast.csv')
    os.makedirs('ml', exist_ok=True)
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['sku', 'week_start', 'forecast_units'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {out_path} with {len(rows)} rows.")

if __name__ == '__main__':
    generate()
