import sys, io, csv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd, re

xlsx_path = r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\Settlement_Optimized_Diversity_Plan.xlsx'
sheets = pd.read_excel(xlsx_path, sheet_name=None)
all_plots = []

def tf(v):
    try:
        f = float(v)
        return None if f != f else round(f, 1)
    except:
        return None

def ts(v):
    s = str(v).strip()
    return None if s in ['nan', 'None', ''] else s

STYLE_MAP = {
    'Modern Flat-Roof': 'Modern Flat-Roof',
    'Barnhouse': 'Barnhouse',
    'A-Frame': 'A-Frame',
    'Barn_157': 'Barnhouse',
    'Barn_85': 'Barn 85',
    'Barn_115': 'Barn 115',
    'Barn_55': 'Barn 55',
    'A_55': 'A-Frame',
}

for sname, df in sheets.items():
    hr = df.iloc[0]
    dd = df.iloc[1:].reset_index(drop=True)

    def fc(kw, start=0):
        for i in range(start, len(hr)):
            if kw in str(hr.iloc[i]):
                return i
        return None

    seen_starts = set()
    cur = 0
    while cur < len(hr):
        cid = fc('კოდი', cur)
        if cid is None or cid in seen_starts:
            break
        seen_starts.add(cid)
        car = fc('ფართობი', cid)
        clp = fc('1მ2', cid)
        cst = fc('სტილი', cid)
        csq = fc('ფართი', cid + 1) if cid + 1 < len(hr) else None
        crt = fc('დღიური', cid)
        cr  = fc('ROI', cid)
        cinv = fc('საინვ', cid)

        for _, row in dd.iterrows():
            code = ts(row.iloc[cid])
            if not code:
                continue
            if not any(code.startswith(p) for p in ['LA', 'LB', 'LC', 'LD']):
                continue
            style_raw = ts(row.iloc[cst]) if cst else None
            style = STYLE_MAP.get(style_raw, style_raw or 'Barnhouse')
            sqm = tf(row.iloc[csq]) if csq else None
            if sqm is None:
                sqm = {'Modern Flat-Roof': 145, 'Barn 115': 115, 'Barnhouse': 115,
                       'Barn 85': 85, 'Barn 55': 55, 'A-Frame': 55}.get(style, 115)

            area = tf(row.iloc[car]) if car else None
            lp = tf(row.iloc[clp]) if clp else None
            dr = tf(row.iloc[crt]) if crt else None
            roi = tf(row.iloc[cr]) if cr else None
            inv = tf(row.iloc[cinv]) if cinv else None

            bc = 1750
            if inv and area and lp and sqm and sqm > 0:
                land_cost = (area or 0) * (lp or 0)
                bc_calc = (inv - land_cost) / sqm
                if 1200 < bc_calc < 2500:
                    bc = round(bc_calc)

            all_plots.append({
                'id': code, 'zone': code[:2],
                'area': area or 500,
                'sqm': sqm,
                'style': style,
                'land_price': lp or 100,
                'build_cost': bc,
                'daily_rent': dr or 200,
                'roi_file': roi or 10.0,
                'ah_price': '',
                'status': 'free',
                'notes': ''
            })
        cur = cid + 20

# Apart Hotel: 75 Studios (35m²) + 25 Junior Suites (50m²)
for i in range(1, 76):
    num = str(i).zfill(2)
    base_price = 45000 + (i % 5) * 500
    all_plots.append({
        'id': f'AH-S-{num}', 'zone': 'AH',
        'area': 35, 'sqm': 35, 'style': 'Studio 35m²',
        'land_price': 0, 'build_cost': 0, 'daily_rent': 130,
        'roi_file': 21.5, 'ah_price': base_price,
        'status': 'free', 'notes': ''
    })

for i in range(1, 26):
    num = str(i).zfill(2)
    base_price = 75000 + (i % 4) * 2000
    all_plots.append({
        'id': f'AH-JS-{num}', 'zone': 'AH',
        'area': 50, 'sqm': 50, 'style': 'Junior Suite 50m²',
        'land_price': 0, 'build_cost': 0, 'daily_rent': 190,
        'roi_file': 20.5, 'ah_price': base_price,
        'status': 'free', 'notes': ''
    })

# Write CSV for Google Sheets
csv_path = r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\green_canyon_inventory.csv'
fieldnames = ['id','zone','area','sqm','style','land_price','build_cost','daily_rent','roi_file','ah_price','status','notes']

with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_plots)

print(f'CSV saved: {len(all_plots)} rows')
print(f'Path: {csv_path}')
print('\nColumns:', fieldnames)
print('\nFirst 3 rows:')
for p in all_plots[:3]:
    print(p)
