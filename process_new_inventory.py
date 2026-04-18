import pandas as pd
import re

input_csv = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\new_unprocessed_inventory.csv"
output_csv = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\master_inventory_v2.csv"

raw_data = pd.read_csv(input_csv, header=None, names=['Comments', 'Type Mark', 'Area', 'Count'])

clean_rows = []
other_rows = []

for index, row in raw_data.iterrows():
    type_mark = str(row['Type Mark']).strip()
    comments = str(row['Comments']).strip()
    area_str = str(row['Area']).strip()
    
    # Filter valid residential types
    if type_mark in ['LA', 'LB', 'LC', 'LD']:
        if pd.isna(comments) or comments == 'nan' or not comments.isdigit():
            # if the Plot Number (Comments column) is not a digit, skip (it might be header)
            continue
            
        plot_number_int = int(comments)
        
        # Parse area
        area_num = 0.0
        try:
            # remove 'm2', 'm', ' ', etc.
            area_clean = re.sub(r'[^\d\.]', '', area_str)
            area_num = float(area_clean)
        except:
            pass
            
        full_plot_id = f"{type_mark}{plot_number_int}"
        
        clean_rows.append({
            'Zone': type_mark,
            'Number': plot_number_int,
            'Full_ID': full_plot_id,
            'Area_sqm': area_num
        })
    elif type_mark.startswith('F') or type_mark in ['FV-01', 'FR-01', 'FC-01']:
         other_rows.append({
             'Type': comments,
             'Code': type_mark,
             'Area_sqm': re.sub(r'[^\d\.]', '', area_str)
         })

df = pd.DataFrame(clean_rows)
# Sort by Zone (LA, LB, LC, LD) then Number
df = df.sort_values(by=['Zone', 'Number']).reset_index(drop=True)

df.to_csv(output_csv, index=False, encoding='utf-8')

print("--- RESIDENTIAL PLOTS ---")
print(f"Total residential plots: {len(df)}")
zone_counts = df['Zone'].value_counts()
print("\nCounts by Zone:")
print(zone_counts)

print("\n--- NON-RESIDENTIAL INFRASTRUCTURE ---")
df_other = pd.DataFrame(other_rows)
print(df_other)

# Checking plot counts by sizes as requested previously:
# 0-400 -> 65m2
# 400-600 -> 120m2
# >600 -> 180m2
sizes = []
for a in df['Area_sqm']:
    if a < 400:
        sizes.append('65 m2')
    elif a <= 600:
        sizes.append('120 m2')
    else:
        sizes.append('180 m2')

df['Cottage_Type'] = sizes
print("\nCottage Size Distribution:")
print(df['Cottage_Type'].value_counts())
