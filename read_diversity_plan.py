import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\Settlement_Optimized_Diversity_Plan.xlsx"

try:
    # Read all sheets
    sheet_to_df_map = pd.read_excel(excel_path, sheet_name=None)
    
    print(f"File: {excel_path}")
    print(f"Sheets found: {list(sheet_to_df_map.keys())}\n")
    
    for sheet_name, df in sheet_to_df_map.items():
        print(f"--- Sheet: {sheet_name} ---")
        print(df.to_string(index=False))
        print("\n" + "="*50 + "\n")
        
except Exception as e:
    print(f"Error reading Excel file: {e}")
