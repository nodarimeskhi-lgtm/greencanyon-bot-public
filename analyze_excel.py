import pandas as pd
df = pd.read_excel(r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\Settlement_Optimized_Diversity_Plan.xlsx')
with open(r'c:\Users\Nodar\2026 antigraviti\excel_out.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total Rows: {len(df)}\n")
    f.write(f"Columns: {', '.join(df.columns)}\n\n")
    area_col = next((c for c in df.columns if 'area' in c.lower() or 'ფართობი' in c.lower() or 'plot' in c.lower() or 'sqm' in c.lower()), None)
    if area_col:
        f.write(f"Area Distribution ({area_col}):\n")
        f.write(str(df.groupby(area_col).size()))
    else:
        f.write("No explicit area column found.")
