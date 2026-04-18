import pandas as pd
import os
import re

# Paths
csv_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\master_inventory_v2.csv"
output_xlsx = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\Land_Plot_and_Cottage_Pricing_Full_Official_V2.xlsx"

def get_cottage_type(area):
    if area >= 800:
        return "LUX Grand Villa", 440000
    elif area >= 600:
        return "Comfort Chalet", 264000
    elif area >= 450:
        return "Eco Cottage", 187000
    elif area >= 400:
        return "Alpine 1 Bed", 105000
    else:
        return "Alpine Studio", 77000

def generate_excel():
    # Load and Clean Data
    df_raw = pd.read_csv(csv_path)
    
    plot_list = []
    
    for _, row in df_raw.iterrows():
        zone = row['Zone']
        num = row['Number']
        full_id = f"{zone}-{num}"
        area = row['Area_sqm']
        
        c_type, c_price = get_cottage_type(area)
        land_price = int(area * 50)
        total = c_price + land_price
        
        plot_list.append({
            'Zone': zone,
            'Code_Num': num,
            'ნაკვეთის კოდი': full_id,
            'ფართი (მ2)': area,
            'კოტეჯის ტიპი': c_type,
            'კოტეჯის ფასი ($)': c_price,
            'მიწის ფასი ($)': land_price,
            'ჯამი (Turnkey) ($)': total
        })

    # Create DataFrame
    df = pd.DataFrame(plot_list)
    
    # Sort
    df = df.sort_values(by=['Zone', 'Code_Num'])
    
    # Remove internal sorting columns
    df = df.drop(columns=['Zone', 'Code_Num'])
    
    # Save to Excel
    with pd.ExcelWriter(output_xlsx, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Inventory List V2')
        
        workbook = writer.book
        worksheet = writer.sheets['Inventory List V2']
        
        for i, col in enumerate(df.columns):
            column_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
            worksheet.column_dimensions[chr(65 + i)].width = column_len

    print(f"Excel generated: {output_xlsx} with {len(df)} plots.")

if __name__ == "__main__":
    generate_excel()
