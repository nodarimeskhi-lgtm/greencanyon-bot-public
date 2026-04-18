import pandas as pd
import json

file_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\Settlement_Optimized_Diversity_Plan.xlsx"

try:
    xl = pd.ExcelFile(file_path)
    result = {}
    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        result[sheet] = {
            "columns": list(df.columns),
            "head": df.head(10).to_dict(orient="records")
        }
    
    with open("excel_dump.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Successfully dumped right sheets.")
except Exception as e:
    print(f"Error: {e}")
