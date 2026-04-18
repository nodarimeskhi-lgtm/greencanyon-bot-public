import pandas as pd
import json
import math

df = pd.read_excel('ახალი.xlsx')

plots = []

def safe_float(val):
    try:
        return float(val) if pd.notna(val) else 0.0
    except ValueError:
        return 0.0

for _, row in df.iterrows():
    plot_id = str(row['კანიონის პირი'])
    if pd.isna(plot_id) or plot_id.strip() == '' or 'ნაკვეთის' in plot_id:
        continue
        
    # Standard Offer
    area = safe_float(row['Unnamed: 1'])
    if area == 0:
        continue
    land_price = safe_float(row['Unnamed: 2'])
    style = str(row['Unnamed: 4']) if pd.notna(row['Unnamed: 4']) else ""
    sqm = safe_float(row['Unnamed: 5'])
    build_cost = safe_float(row['Unnamed: 6'])
    
    # Promo Offer
    promo_style = str(row['Unnamed: 15']) if pd.notna(row['Unnamed: 15']) else ""
    promo_sqm = safe_float(row['Unnamed: 16'])
    promo_build_cost = safe_float(row['Unnamed: 17'])

    
    item = {
        "id": plot_id,
        "area": area,
        "land_price": land_price,
        "daily_rent": float(row['Unnamed: 27']) if pd.notna(row['Unnamed: 27']) else 0,
        "style": style,
        "sqm": sqm,
        "build_cost": build_cost
    }
    
    if promo_style and promo_style.lower() != 'nan':
        item["promo_style"] = promo_style
        item["promo_sqm"] = promo_sqm
        item["promo_build_cost"] = promo_build_cost
        
    plots.append(item)

with open('plots_wix_data.json', 'w', encoding='utf-8') as f:
    json.dump(plots, f, ensure_ascii=False, indent=2)

print("Extracted", len(plots), "plots to plots_wix_data.json")
