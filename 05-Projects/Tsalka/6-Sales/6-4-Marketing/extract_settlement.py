import sys, io, json, collections
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

    # Process each band (up to 2 side-by-side tables per sheet)
    seen_starts = set()
    for try_start in range(0, len(hr)):
        cid = fc('კოდი', try_start)
        if cid is None or cid in seen_starts:
            break
        seen_starts.add(cid)
        car = fc('ფართობი', cid)
        clp = fc('1მ2', cid)
        cst = fc('სტილი', cid)
        csq = fc('ფართი', cid + 1) if cid + 1 < len(hr) else None
        crt = fc('დღიური', cid)
        cr = fc('ROI', cid)

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

        # Advance to find next band
        next_start = cid + 5
        if next_start >= len(hr):
            break
        try_start = next_start

print(f'TOTAL PLOTS: {len(all_plots)}')
zones = dict(collections.Counter(p['zone'] for p in all_plots))
print('By zone:', zones)
print('By style:', dict(collections.Counter(p['style'] for p in all_plots)))
print()
for p in all_plots[:5]:
    print(p)

with open(r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\plots_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_plots, f, ensure_ascii=False, indent=2)
print('\nSaved plots_data.json')
