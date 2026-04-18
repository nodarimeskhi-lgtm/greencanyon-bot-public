import pandas as pd

file_path = r"c:\Users\Nodar\2026 antigraviti\ახალი.xlsx"
output_path = r"c:\Users\Nodar\2026 antigraviti\axali_analysis.txt"

try:
    df = pd.read_excel(file_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Total Rows: {len(df)}\n")
        f.write(f"Columns: {', '.join(df.columns.astype(str))}\n\n")
        
        f.write("--- Data Sample ---\n")
        f.write(df.head().to_string() + "\n\n")
        
        # Try to identify useful columns dynamically
        # Let's look for type, area, price
        price_cols = [c for c in df.columns if 'price' in str(c).lower() or 'ფასი' in str(c).lower() or 'ღირებულება' in str(c).lower()]
        area_cols = [c for c in df.columns if 'area' in str(c).lower() or 'ფართობი' in str(c).lower() or 'sqm' in str(c).lower()]
        type_cols = [c for c in df.columns if 'type' in str(c).lower() or 'ტიპი' in str(c).lower() or 'status' in str(c).lower()]
        
        f.write(f"Potential Price Columns: {price_cols}\n")
        f.write(f"Potential Area Columns: {area_cols}\n")
        f.write(f"Potential Type/Status Columns: {type_cols}\n\n")
        
        if type_cols:
            col = type_cols[0]
            f.write(f"Breakdown by {col}:\n")
            f.write(df.groupby(col).size().to_string() + "\n\n")
            
        if area_cols:
            col = area_cols[0]
            f.write(f"Breakdown by {col}:\n")
            f.write(df.groupby(col).size().to_string() + "\n\n")
            
        if price_cols:
            col = price_cols[-1] # Usually the last one is total price
            f.write(f"Summary of '{col}':\n")
            # f.write(df[col].describe().to_string() + "\n")
            
            # Convert to numeric, errors='coerce' to handle strings
            df[col] = pd.to_numeric(df[col], errors='coerce')
            f.write(f"Total Sum: {df[col].sum()}\n")
            f.write(f"Average: {df[col].mean()}\n")
            f.write(f"Min: {df[col].min()}\n")
            f.write(f"Max: {df[col].max()}\n")

except Exception as e:
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Error processing excel file: {str(e)}\n")
