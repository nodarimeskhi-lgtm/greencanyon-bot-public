import pandas as pd
import json

def to_float(val):
    try:
        if pd.isna(val): return 0.0
        # Remove any currency symbols, commas, spaces
        if isinstance(val, str):
            val = val.replace('$', '').replace(',', '').replace(' ', '').strip()
            if not val: return 0.0
        return float(val)
    except:
        return 0.0

try:
    excel_path = r'c:\Users\Nodar\2026 antigraviti\08-Sales-Marketing\2026.xlsx'
    df1 = pd.read_excel(excel_path, sheet_name='Sheet1')
    
    plots_data = []
    
    for idx, row in df1.iterrows():
        plot_id = str(row.get('ნაკვეთის კოდი', '')).strip()
        if pd.isna(plot_id) or plot_id == 'nan' or not plot_id or plot_id == 'ნაკვეთის კოდი':
            continue
            
        plot_info = {
            'id': plot_id,
            'land_area': to_float(row.get('ნაკვეთის ფართობი (მ2)')),
            'land_price_sqm': to_float(row.get('მიწის 1მ2 ფასი')),
            'land_total': to_float(row.get('მიწის ღირებულება $')),
            'house_style': str(row.get('სახლის სტილი', '')).replace('nan', ''),
            'house_area': to_float(row.get('სახლის ფართი (მ2)')),
            'house_price_sqm': to_float(row.get('ობიექტის რეალიზაციის ფასი 1 მ2  $')),
            'total_investment': to_float(row.get('საინვესტიცო ღირებულება')),
            
            'financial': {
                'reservation': to_float(row.get('ბეი - რეზერვი $')),
                'downpayment_10': to_float(row.get('პირველი შენატანი 10%')),
                'post_handover_20': to_float(row.get('პოსტ-ჰენდოვერი (20%)')),
                'monthly_36': to_float(row.get('ყოველთვიური (36 თვე)')),
                'promo_8_percent': to_float(row.get('სააქციო შეთავაზება 8% გარანტირებული უკუგება 2 წელი')),
                'daily_rent': to_float(row.get('დღიური ქირის ფასი ($)')),
                'passive_income': to_float(row.get('პასიური წლიური 45% დათვირთვით შემოსავალი')),
                'roi_percent': to_float(row.get('პესიმისტური Rental ROI %')),
                'payback_years': to_float(row.get('პესიმისტური უკუგება (წელი)'))
            }
        }
        plots_data.append(plot_info)

    with open(r'c:\Users\Nodar\2026 antigraviti\plots_data_2026.json', 'w', encoding='utf-8') as f:
        json.dump(plots_data, f, ensure_ascii=False, indent=2)
    print(f"Parsed {len(plots_data)} plots from standard sheet")
    
    # Process Sheet2 (Alternatives)
    df2 = pd.read_excel(excel_path, sheet_name='Sheet2')
    df2.columns = df2.iloc[0]
    df2 = df2[1:]
    
    alt_data = []
    for idx, row in df2.iterrows():
        plot_id = str(row.get('ნაკვეთის კოდი', '')).strip()
        if pd.isna(plot_id) or plot_id == 'nan' or not plot_id or plot_id == 'ნაკვეთის კოდი':
            continue
            
        alt_info = {
            'id': plot_id,
            'land_area': to_float(row.get('ნაკვეთის ფართობი (მ2)')),
            'house_style': str(row.get('სახლის სტილი', '')).replace('nan', ''),
            'house_area': to_float(row.get('სახლის ფართი (მ2)')),
            'total_investment': to_float(row.get('საინვესტიცო ღირებულება')),
            
            'financial': {
                'reservation': to_float(row.get('ბეი - რეზერვი $')),
                'downpayment_10': to_float(row.get('პირველი შენატანი 10%')),
                'monthly_36': to_float(row.get('ყოველთვიური (36 თვე)')),
                'roi_percent': to_float(row.get('პესიმისტური Rental ROI %'))
            }
        }
        alt_data.append(alt_info)
        
    with open(r'c:\Users\Nodar\2026 antigraviti\alt_plots_data_2026.json', 'w', encoding='utf-8') as f:
        json.dump(alt_data, f, ensure_ascii=False, indent=2)
    print(f"Parsed {len(alt_data)} plots from alternative sheet")

except Exception as e:
    import traceback
    traceback.print_exc()
