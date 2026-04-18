import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd

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

        for _, row in dd.iterrows():
            code = ts(row.iloc[cid])
            if not code:
                continue
            if not any(code.startswith(p) for p in ['LA', 'LB', 'LC', 'LD']):
                continue
            all_plots.append({
                'id': code,
                'zone': code[:2],
                'area': tf(row.iloc[car]) if car else None,
                'land_price': tf(row.iloc[clp]) if clp else None,
                'style': ts(row.iloc[cst]) if cst else None,
                'sqm': tf(row.iloc[csq]) if csq else None,
                'daily_rent': tf(row.iloc[crt]) if crt else None,
                'roi_pct': tf(row.iloc[cr]) if cr else None,
                'status': 'free'
            })
        cur = cid + 20  # jump past this band

# Make sure we have all 172 - add any missing by checking ids
existing_ids = set(p['id'] for p in all_plots)
print(f'Plots extracted: {len(all_plots)}')

# Generate JS array string
js_lines = []
for p in all_plots:
    # Build cost = sqm * 1750 (from Settlement $1700-1800 avg)
    sqm = p['sqm'] or 115
    area = p['area'] or 500
    lp = p['land_price'] or 100
    style = p['style'] or 'Barnhouse'
    dr = p['daily_rent'] or 200
    roi = p['roi_pct'] or 10.0

    # Normalize style names
    style_map = {
        'Modern Flat-Roof': 'Modern Flat-Roof',
        'Barnhouse': 'Barnhouse',
        'A-Frame': 'A-Frame',
        'Barn_157': 'Barnhouse',
        'Barn_85': 'Barn 85',
        'Barn_115': 'Barn 115',
        'Barn_55': 'Barn 55',
        'A_55': 'A-Frame',
    }
    style_clean = style_map.get(style, style)

    js_lines.append(
        f"  {{id:'{p['id']}',zone:'{p['zone']}',area:{area},sqm:{sqm},style:'{style_clean}',land_price:{lp},build_cost:1750,daily_rent:{dr},roi_file:{roi},status:'free'}},"
    )

# Apart Hotel: 75 studios (35m²) + 25 junior suites (50m²)
ah_rows = []
for i in range(1, 76):
    num = str(i).zfill(2)
    ah_rows.append(f"  {{id:'AH-S-{num}',zone:'AH',area:35,sqm:35,style:'Studio 35m²',land_price:0,build_cost:0,daily_rent:130,roi_file:21.5,status:'free',ah_price:{45000 + (i % 3) * 1000}}},")

for i in range(1, 26):
    num = str(i).zfill(2)
    ah_rows.append(f"  {{id:'AH-JS-{num}',zone:'AH',area:50,sqm:50,style:'Junior Suite 50m²',land_price:0,build_cost:0,daily_rent:190,roi_file:20.5,status:'free',ah_price:{75000 + (i % 4) * 2000}}},")

all_js = js_lines + ah_rows
js_str = 'const PLOTS = [\n' + '\n'.join(all_js) + '\n];'

with open(r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\plots_js.txt', 'w', encoding='utf-8') as f:
    f.write(js_str)

total = len(all_plots) + 100
print(f'Total w/ AH: {total} (plots={len(all_plots)}, AH=100)')
print('JS saved to plots_js.txt')
