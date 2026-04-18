import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\Settlement_Optimized_Diversity_Plan.xlsx"

try:
    df = pd.read_excel(excel_path, header=1)
    
    # The columns for the second row start around index 16
    # Let's cleanly print the second row data where alternative is 2x
    print("--- POTENTIAL DENSITY RISKS IN SECOND ROW ---")
    
    # Indices based on previous output:
    # 16: ნაკვეთის კოდი (მეორე ზოლი)
    # 17: ნაკვეთის ფართობი (მ2)
    # 24: ალტერნატიული შეთავაზება
    
    col_code = df.columns[16]
    col_area = df.columns[17]
    col_alt = df.columns[24]
    
    risky_plots = []
    
    for index, row in df.iterrows():
        code = str(row.iloc[16])
        if pd.isna(code) or code == 'nan':
            continue
            
        area = row.iloc[17]
        alt = str(row.iloc[24])
        
        # If alternative proposes 2 houses on a relatively small plot
        if '2 x' in alt or '2x' in alt:
            risky_plots.append((code, area, alt))
            
    # Sort by area ascending to find the smallest plots with 2 houses
    risky_plots.sort(key=lambda x: float(x[1]) if str(x[1]).replace('.','',1).isdigit() else 9999)
    
    for rp in risky_plots:
        print(f"Plot Code: {rp[0]} | Area: {rp[1]} m2 | Proposed Alternative: {rp[2]}")
        
except Exception as e:
    print(f"Error: {e}")
