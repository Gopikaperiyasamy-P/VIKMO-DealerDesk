import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge

def load_data():
    sales = pd.read_csv('data/sales_history.csv')
    sales['week_start'] = pd.to_datetime(sales['week_start'])
    
    promo = pd.read_csv('data/promo_calendar.csv')
    promo['week_start'] = pd.to_datetime(promo['week_start'])
    
    lead = pd.read_csv('data/lead_times.csv')
    
    fest = pd.read_csv('data/festival_calendar.csv')
    fest['date'] = pd.to_datetime(fest['date'])
    diwali_dates = fest[fest['festival'] == 'Diwali']['date'].values
    
    return sales, promo, lead, diwali_dates

def get_diwali_distance(week_date, diwali_dates):
    # returns signed weeks to nearest Diwali (negative = before Diwali, positive = after)
    min_dist_days = 9999
    best_diff_weeks = 0
    for d in diwali_dates:
        diff_days = (pd.to_datetime(week_date) - pd.to_datetime(d)).days
        if abs(diff_days) < abs(min_dist_days):
            min_dist_days = diff_days
            best_diff_weeks = diff_days / 7.0
    return best_diff_weeks

def evaluate_models():
    sales, promo, lead, diwali_dates = load_data()
    all_skus = lead['sku'].tolist()
    
    # Historical cutoff dates for 4-week evaluation windows
    val_cutoffs = [
        pd.to_datetime('2026-05-25'),
        pd.to_datetime('2026-06-22'),
        pd.to_datetime('2026-07-20'),
        pd.to_datetime('2026-08-24'),
    ]
    
    models = ['Last_Value', 'Recent_4w_Mean', 'Recent_12w_Mean', 'Same_Week_Last_Year', 'Gradient_Boosting_Hybrid']
    scores = {m: [] for m in models}
    
    for cutoff in val_cutoffs:
        train = sales[sales['week_start'] < cutoff].copy()
        test = sales[(sales['week_start'] >= cutoff) & (sales['week_start'] < cutoff + pd.Timedelta(weeks=4))].copy()
        
        # Test weeks
        test_weeks = sorted(test['week_start'].unique())
        if len(test_weeks) != 4:
            continue
            
        # 1. Baseline: Last Value
        last_val_preds = []
        for _, row in test.iterrows():
            sku = row['sku']
            sub = train[train['sku'] == sku].sort_values('week_start')
            pred = sub['units_sold'].iloc[-1] if len(sub) > 0 else 0
            last_val_preds.append(pred)
        scores['Last_Value'].append(np.mean(np.abs(test['units_sold'] - last_val_preds)))
        
        # 2. Baseline: Recent 4-week mean
        mean4_preds = []
        for _, row in test.iterrows():
            sku = row['sku']
            sub = train[train['sku'] == sku].sort_values('week_start')
            pred = sub['units_sold'].tail(4).mean() if len(sub) > 0 else 0
            mean4_preds.append(pred)
        scores['Recent_4w_Mean'].append(np.mean(np.abs(test['units_sold'] - mean4_preds)))
        
        # 3. Baseline: Recent 12-week mean
        mean12_preds = []
        for _, row in test.iterrows():
            sku = row['sku']
            sub = train[train['sku'] == sku].sort_values('week_start')
            pred = sub['units_sold'].tail(12).mean() if len(sub) > 0 else 0
            mean12_preds.append(pred)
        scores['Recent_12w_Mean'].append(np.mean(np.abs(test['units_sold'] - mean12_preds)))
        
        # 4. Baseline: Same week last year
        swly_preds = []
        for _, row in test.iterrows():
            sku = row['sku']
            target_prev = row['week_start'] - pd.DateOffset(years=1)
            sub = train[(train['sku'] == sku) & (train['week_start'] >= target_prev - pd.Timedelta(days=4)) & (train['week_start'] <= target_prev + pd.Timedelta(days=4))]
            if len(sub) > 0:
                pred = sub['units_sold'].iloc[0]
            else:
                # Fallback to recent 4w mean for new SKUs
                sub_all = train[train['sku'] == sku].sort_values('week_start')
                pred = sub_all['units_sold'].tail(4).mean() if len(sub_all) > 0 else 0
            swly_preds.append(pred)
        scores['Same_Week_Last_Year'].append(np.mean(np.abs(test['units_sold'] - swly_preds)))
        
        # 5. Hybrid Model: Gradient Boosting with Promo, Diwali alignment, and lag dynamics
        gb_preds = []
        # Fit per-SKU or pooled model with SKU features
        # Let's build features on train
        features = []
        targets = []
        
        sku_dummies = {s: i for i, s in enumerate(all_skus)}
        
        # Feature extraction
        for sku in all_skus:
            sub = train[train['sku'] == sku].sort_values('week_start').reset_index(drop=True)
            if len(sub) < 6:
                continue
            for i in range(12, len(sub)):
                w = sub.loc[i, 'week_start']
                diwali_diff = get_diwali_distance(w, diwali_dates)
                f = [
                    sub.loc[i-4, 'units_sold'],
                    sub.loc[i-5, 'units_sold'],
                    sub.loc[i-6, 'units_sold'],
                    sub.loc[i-12:i-4, 'units_sold'].mean(),
                    sub.loc[i-8:i-4, 'units_sold'].mean(),
                    sub.loc[i, 'promo_flag'],
                    diwali_diff,
                    np.exp(-0.5 * (diwali_diff / 2.0)**2), # gaussian diwali bell
                    w.month,
                    sku_dummies[sku],
                ]
                features.append(f)
                targets.append(sub.loc[i, 'units_sold'])
                
        if len(features) > 0:
            reg = GradientBoostingRegressor(n_estimators=60, max_depth=4, learning_rate=0.08, random_state=42)
            reg.fit(features, targets)
            
            for _, row in test.iterrows():
                sku = row['sku']
                sub = train[train['sku'] == sku].sort_values('week_start').reset_index(drop=True)
                if len(sub) < 6:
                    pred = sub['units_sold'].mean() if len(sub) > 0 else 0
                else:
                    w = row['week_start']
                    diwali_diff = get_diwali_distance(w, diwali_dates)
                    f = [[
                        sub['units_sold'].iloc[-1],
                        sub['units_sold'].iloc[-2] if len(sub) > 1 else sub['units_sold'].iloc[-1],
                        sub['units_sold'].iloc[-3] if len(sub) > 2 else sub['units_sold'].iloc[-1],
                        sub['units_sold'].tail(8).mean(),
                        sub['units_sold'].tail(4).mean(),
                        row['promo_flag'],
                        diwali_diff,
                        np.exp(-0.5 * (diwali_diff / 2.0)**2),
                        w.month,
                        sku_dummies[sku],
                    ]]
                    pred = max(0.0, float(reg.predict(f)[0]))
                gb_preds.append(pred)
        else:
            gb_preds = mean4_preds
            
        scores['Gradient_Boosting_Hybrid'].append(np.mean(np.abs(test['units_sold'] - gb_preds)))
        
    print("=== CHRONOLOGICAL LEAKAGE-FREE VALIDATION RESULTS (MAE) ===")
    for m in models:
        avg_mae = np.mean(scores[m])
        print(f"{m:26}: Mean MAE = {avg_mae:.3f} across {len(val_cutoffs)} windows")

if __name__ == "__main__":
    evaluate_models()
