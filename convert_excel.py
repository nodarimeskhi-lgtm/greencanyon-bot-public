import pandas as pd
import os

# Absolute path to the Excel file
file_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-3-Agency-Outreach\ფინანსური ანალიზი.xlsx"
output_csv = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\full_inventory.csv"

try:
    # Read the Excel file
    # We might need to specify the engine if openpyxl is not default
    df = pd.read_excel(file_path)
    
    # Save to CSV with UTF-8 encoding
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Successfully converted to CSV: {output_csv}")
    print(df.head(10).to_string())
except Exception as e:
    print(f"Error: {e}")
