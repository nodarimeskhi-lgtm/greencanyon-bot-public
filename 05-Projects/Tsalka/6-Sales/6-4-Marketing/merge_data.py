import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd, re

# ── 1. Read Settlement Excel ──
xlsx_path = r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\Settlement_Optimized_Diversity_Plan.xlsx'
sheets = pd.read_excel(xlsx_path, sheet_name=None)

STYLE_MAP = {
    'Modern Flat-Roof': 'Modern Flat-Roof', 'Barnhouse': 'Barnhouse',
    'A-Frame': 'A-Frame', 'Barn_157': 'Barnhouse', 'Barn_85': 'Barn 85',
    'Barn_115': 'Barn 115', 'Barn_55': 'Barn 55', 'A_55': 'A-Frame',
}
SQM_BY_STYLE = {
    'Modern Flat-Roof': 145, 'Barnhouse': 115, 'Barn 115': 115,
    'Barn 85': 85, 'Barn 55': 55, 'A-Frame': 55,
}

def tf(v):
    try: f = float(v); return None if f != f else round(f, 1)
    except: return None

def ts(v):
    s = str(v).strip()
    return None if s in ['nan','None',''] else s

inventory = []
for sname, df in sheets.items():
    hr = df.iloc[0]; dd = df.iloc[1:].reset_index(drop=True)
    def fc(kw, start=0):
        for i in range(start, len(hr)):
            if kw in str(hr.iloc[i]): return i
        return None
    seen, cur = set(), 0
    while cur < len(hr):
        cid = fc('კოდი', cur)
        if cid is None or cid in seen: break
        seen.add(cid)
        car=fc('ფართობი',cid); clp=fc('1მ2',cid); cst=fc('სტილი',cid)
        csq=fc('ფართი',cid+1) if cid+1<len(hr) else None
        crt=fc('დღიური',cid); cr=fc('ROI',cid); cinv=fc('საინვ',cid)
        for _, row in dd.iterrows():
            code = ts(row.iloc[cid])
            if not code or not any(code.startswith(p) for p in ['LA','LB','LC','LD','AH']): continue
            style_raw = ts(row.iloc[cst]) if cst else None
            style = STYLE_MAP.get(style_raw, style_raw)
            sqm = tf(row.iloc[csq]) if csq else SQM_BY_STYLE.get(style, 115)
            if not code.startswith('AH') and not style: style = 'Barnhouse'
            area = tf(row.iloc[car]) if car else None
            lp = tf(row.iloc[clp]) if clp else None
            dr = tf(row.iloc[crt]) if crt else None
            roi = tf(row.iloc[cr]) if cr else None
            inv = tf(row.iloc[cinv]) if cinv else None
            bc = 1750
            if inv and area and lp and sqm and sqm > 0:
                lc = (area or 0)*(lp or 0); bc_c = (inv-lc)/sqm
                if 1200 < bc_c < 2500: bc = round(bc_c)
            ah_price = None
            if code.startswith('AH'):
                ah_price = inv
                bc = 0
                lp = 0
                if not style:
                    style = f'Studio {sqm}m²' if sqm and sqm < 40 else f'Junior Suite {sqm}m²'

            inventory.append({'id':code,'zone':code[:2],'area':area or 500 if not code.startswith('AH') else 0,
                'sqm':sqm or 115,'style':style,'land_price':lp or 100 if not code.startswith('AH') else 0,
                'build_cost':bc,'daily_rent':dr or 200,
                'roi_file':roi or 10.0,'ah_price':ah_price,'status':'free','notes':''})
        cur = cid + 20

# Apart hotels are now directly loaded from Excel

# ── 2. Load map plot data (latlng) ──
MAP_HTML = r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\interactive_map_leaflet.html'
with open(MAP_HTML, 'r', encoding='utf-8') as f:
    mhtml = f.read()

# Extract PLOT_DATA JSON from the map file
m = re.search(r'const PLOT_DATA = (\[.*?\]);', mhtml, re.DOTALL)
map_plot_data = json.loads(m.group(1)) if m else []
print(f'Map plots: {len(map_plot_data)}')

# Merge latlng into inventory
latlng_by_id = {p['id']: p['latlng'] for p in map_plot_data}
for p in inventory:
    p['latlng'] = latlng_by_id.get(p['id'])

# ── 3. Build JS data strings ──
inv_js_lines = []
for p in inventory:
    ll = f"[{p['latlng'][0]},{p['latlng'][1]}]" if p['latlng'] else 'null'
    ap = p['ah_price'] if p['ah_price'] else 'null'
    inv_js_lines.append(
        f"  {{id:'{p['id']}',zone:'{p['zone']}',area:{p['area']},"
        f"sqm:{p['sqm']},style:'{p['style']}',land_price:{p['land_price']},"
        f"build_cost:{p['build_cost']},daily_rent:{p['daily_rent']},"
        f"roi_file:{p['roi_file']},ah_price:{ap},"
        f"status:'free',notes:'',latlng:{ll}}},"
    )

inv_js = 'const INVENTORY = [\n' + '\n'.join(inv_js_lines) + '\n];'

print(f'Total inventory: {len(inventory)}')
print(f'With latlng: {sum(1 for p in inventory if p["latlng"])}')

# Save
with open(r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\inventory_js.txt',
          'w', encoding='utf-8') as f:
    f.write(inv_js)
print('inventory_js.txt saved')
