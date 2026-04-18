import sys, io, json
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
            # derive sqm from style name if missing
            if sqm is None:
                if '157' in (style_raw or '') or '156' in (style_raw or ''):
                    sqm = 145
                elif '115' in (style_raw or ''):
                    sqm = 115
                elif '85' in (style_raw or ''):
                    sqm = 85
                elif '55' in (style_raw or ''):
                    sqm = 55
                elif 'Barnhouse' in (style_raw or ''):
                    sqm = 115
                elif 'A-Frame' in (style_raw or '') or 'A_55' in (style_raw or ''):
                    sqm = 55
                else:
                    sqm = 115

            area = tf(row.iloc[car]) if car else None
            lp = tf(row.iloc[clp]) if clp else None
            dr = tf(row.iloc[crt]) if crt else None
            roi = tf(row.iloc[cr]) if cr else None
            inv = tf(row.iloc[cinv]) if cinv else None

            zone = code[:2]
            # build cost from investment: inv = area*lp + sqm*bc => bc = (inv - area*lp) / sqm
            bc = 1750
            if inv and area and lp and sqm and sqm > 0:
                land_cost = (area or 0) * (lp or 0)
                bc_calc = (inv - land_cost) / sqm
                if 1200 < bc_calc < 2500:
                    bc = round(bc_calc)

            all_plots.append({
                'id': code, 'zone': zone,
                'area': area or 500,
                'sqm': sqm,
                'style': style,
                'land_price': lp or 100,
                'build_cost': bc,
                'daily_rent': dr or 200,
                'roi_file': roi,
                'status': 'free'
            })

        cur = cid + 20

# Generate JS lines for plots
js_plot_lines = []
for p in all_plots:
    line = (f"  {{id:'{p['id']}',zone:'{p['zone']}',area:{p['area']},"
            f"sqm:{p['sqm']},style:'{p['style']}',land_price:{p['land_price']},"
            f"build_cost:{p['build_cost']},daily_rent:{p['daily_rent']},"
            f"roi_file:{p['roi_file'] or 10.0},status:'free'}},")
    js_plot_lines.append(line)

# Apart Hotel: 75 Studios (35m²) + 25 Junior Suites (50m²)
ah_lines = []
for i in range(1, 76):
    num = str(i).zfill(2)
    base_price = 45000 + (i % 5) * 500
    ah_lines.append(
        f"  {{id:'AH-S-{num}',zone:'AH',area:35,sqm:35,style:'Studio 35m²',"
        f"land_price:0,build_cost:0,daily_rent:130,roi_file:21.5,status:'free',ah_price:{base_price}}},"
    )

for i in range(1, 26):
    num = str(i).zfill(2)
    base_price = 75000 + (i % 4) * 2000
    ah_lines.append(
        f"  {{id:'AH-JS-{num}',zone:'AH',area:50,sqm:50,style:'Junior Suite 50m²',"
        f"land_price:0,build_cost:0,daily_rent:190,roi_file:20.5,status:'free',ah_price:{base_price}}},"
    )

all_lines = js_plot_lines + ah_lines
js_block = 'const PLOTS = [\n' + '\n'.join(all_lines) + '\n];'

# Write plots block to file
with open(r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\plots_js.txt', 'w', encoding='utf-8') as f:
    f.write(js_block)

print(f'Plots: {len(all_plots)}, AH: 100, Total: {len(all_plots)+100}')
print(f'JS block chars: {len(js_block)}')

# Now patch the dashboard HTML
html_path = r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\sales_dashboard.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the PLOTS array
pattern = r'const PLOTS = \[[\s\S]*?\];'
new_html = re.sub(pattern, js_block, html, count=1)

if new_html == html:
    print('WARNING: Pattern not matched, could not replace PLOTS!')
else:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print('HTML updated successfully!')
    print(f'File size: {len(new_html)} chars')
