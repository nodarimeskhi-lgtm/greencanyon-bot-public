import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

excel_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\Settlement_Optimized_Diversity_Plan.xlsx"

try:
    df = pd.read_excel(excel_path, sheet_name=0)
    
    print("--- NEW SETTLEMENT DIVERSITY PLAN SUMMARY ---")
    
    total_plots = len(df)
    print(f"Total Plots: {total_plots}")
    
    print("\n--- COTTAGE TYPE DISTRIBUTION ---")
    if 'კოტეჯის ტიპი პირველადი' in df.columns:
        type_col = 'კოტეჯის ტიპი პირველადი'
    elif 'კოტეჯის ტიპი' in df.columns:
        type_col = 'კოტეჯის ტიპი'
    else:
        type_col = df.columns[4] # Guessing based on common structure
        
    print(df[type_col].value_counts())
    
    print("\n--- ALTERNATIVE COTTAGE TYPES ---")
    if 'ალტერნატივა 1 (ტიპი)' in df.columns:
        print(df['ალტერნატივა 1 (ტიპი)'].value_counts())
        
    print("\n--- FINANCIALS (Primary Plan) ---")
    # Finding total price column
    total_price_col = None
    for col in df.columns:
        if 'ჯამი' in str(col) or 'Total' in str(col):
            # pick the first one which is usually the primary total
            total_price_col = col
            break
            
    if total_price_col:
        total_rev = df[total_price_col].sum()
        avg_price = df[total_price_col].mean()
        min_price = df[total_price_col].min()
        max_price = df[total_price_col].max()
        
        print(f"Total Projected Revenue: ${total_rev:,.0f}")
        print(f"Average Turnkey Price: ${avg_price:,.0f}")
        print(f"Price Range: ${min_price:,.0f} - ${max_price:,.0f}")
        
    print("\n--- SAMPLE ROWS (First 5) ---")
    print(df.head().to_string())

except Exception as e:
    print(f"Error: {e}")
