import json
import os
import re

app_dir = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing"
base_dir = r"c:\Users\Nodar\2026 antigraviti"

with open(os.path.join(base_dir, 'plots_data_2026.json'), 'r', encoding='utf-8') as f:
    standard_data = json.load(f)

plots_dict = {p['id']: p for p in standard_data}

with open(os.path.join(app_dir, 'interactive_map.html'), 'r', encoding='utf-8') as f:
    html_content = f.read()

new_panel = """
<div class="cp" style="padding: 20px;">
    <div style="background: var(--p); color: #fff; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
       <h2 data-i18n="info_title" style="margin-bottom:10px; font-size:18px;">Plot Information</h2>
       <div id="plot-id" style="font-size: 24px; font-weight: bold; color: var(--g);">—</div>
    </div>
    
    <div id="plot-data" style="display: none;">
        <div style="margin-bottom: 15px;">
            <div style="font-size: 12px; color: var(--mu);" data-i18n="land_area">Plot Area (m²)</div>
            <div id="v_area" style="font-size: 16px; font-weight: bold;">-</div>
        </div>
        <div style="margin-bottom: 15px;">
            <div style="font-size: 12px; color: var(--mu);" data-i18n="house_area">House Area (m²)</div>
            <div id="v_house" style="font-size: 16px; font-weight: bold;">-</div>
        </div>
        <div style="margin-bottom: 15px;">
            <div style="font-size: 12px; color: var(--mu);" data-i18n="price">Total Investment</div>
            <div id="v_price" style="font-size: 18px; font-weight: bold; color: var(--g);">-</div>
        </div>
        <div style="margin-bottom: 25px;">
            <div style="font-size: 12px; color: var(--mu);" data-i18n="roi">Projected ROI</div>
            <div id="v_roi" style="font-size: 18px; font-weight: bold; color: var(--s);">-</div>
        </div>
        
        <button onclick="openCalc()" style="width: 100%; padding: 15px; background: var(--r); color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px;" data-i18n="btn_calc">
            View Payment Plan & Promo
        </button>
    </div>
    
    <div id="no-sel-msg" style="text-align:center; margin-top:50px; color: var(--mu);" data-i18n="hint">
        Please select a plot on the map
    </div>
</div>
"""

# HTML parsing using split
cp_match = re.search(r'<div class="cp">.*?</div>\s*</div>\s*<script>', html_content, flags=re.DOTALL)
if cp_match:
    html_content = html_content[:cp_match.start()] + new_panel + '\n</div>\n<script>' + html_content[cp_match.end():]

js_injections = f"""
const DATA = {json.dumps(plots_dict, ensure_ascii=False)};

const DICT = {{
    ka: {{
        info_title: "ნაკვეთის ინფო",
        land_area: "მიწის ფართობი (მ²)",
        house_area: "სახლის ფართი (მ²)",
        price: "საინვესტიციო ღირებულება",
        roi: "Rental ROI (პესიმისტური)",
        btn_calc: "გადახდის გრაფიკი და სააქციო კალკულატორი",
        hint: "გთხოვთ აირჩიოთ ნაკვეთი რუკაზე"
    }},
    en: {{
        info_title: "Plot Information",
        land_area: "Plot Area (m²)",
        house_area: "House Area (m²)",
        price: "Total Investment",
        roi: "Rental ROI (Pessimistic)",
        btn_calc: "View Payment Plan & Promo",
        hint: "Please select a plot on the map"
    }},
    ru: {{
        info_title: "Информация об Участке",
        land_area: "Площадь Участка (м²)",
        house_area: "Площадь Дома (м²)",
        price: "Инвестиционная Стоимость",
        roi: "Rental ROI (Пессимистичный)",
        btn_calc: "График Платежей и Акции",
        hint: "Пожалуйста, выберите участок на карте"
    }}
}};

function fmtC(val) {{
    if (!val) return '$0';
    return '$' + Math.round(val).toLocaleString('en-US');
}}

function setLang(l){{
  lang=l;
  document.querySelectorAll('.lb').forEach(b=>b.classList.toggle('on',b.textContent.toLowerCase()===l));
  document.querySelectorAll('[data-i18n]').forEach(el=>{{
      const k=el.getAttribute('data-i18n');
      if(DICT[l] && DICT[l][k]) el.textContent=DICT[l][k];
  }});
}}

function openCalc() {{
    if(cur) {{
        // Open wix_calc.html with parameter
        window.open('wix_calc.html?plot=' + cur.id, '_blank');
    }}
}}

function selectPlot(pid){{
  typeof P !== 'undefined' && P.forEach(d=>{{if(d.id===pid) cur=d;}}); // Set global cur
  if(!cur) {{ cur={{id:pid}}; }} // Fallback
  
  document.querySelectorAll('#dots circle').forEach(c=>c.classList.toggle('active',c.getAttribute('data-id')===pid));
  
  document.getElementById('no-sel-msg').style.display='none';
  document.getElementById('plot-data').style.display='block';
  document.getElementById('plot-id').textContent = pid;
  
  const d = DATA[pid];
  if(d) {{
      document.getElementById('v_area').textContent = d.land_area || '-';
      document.getElementById('v_house').textContent = d.house_area || '-';
      document.getElementById('v_price').textContent = fmtC(d.total_investment);
      document.getElementById('v_roi').textContent = d.financial.roi_percent ? d.financial.roi_percent.toFixed(1) + '%' : '-';
  }} else {{
      document.getElementById('v_area').textContent = 'N/A';
      document.getElementById('v_house').textContent = 'N/A';
      document.getElementById('v_price').textContent = 'N/A';
      document.getElementById('v_roi').textContent = 'N/A';
  }}
  
  if(window.innerWidth<=640)document.querySelector('.cp').scrollIntoView({{behavior:'smooth'}});
}}
"""

func_match = re.search(r'function setLang.*?function selectPlot.*?}', html_content, flags=re.DOTALL)
if func_match:
    html_content = html_content[:func_match.start()] + js_injections + html_content[func_match.end():]

# Also remove calc() and ubdg() from original script safely!
def remove_func(name, content):
    m = re.search(r'function ' + name + r'\(\).*?\}', content, flags=re.DOTALL)
    if m:
        return content[:m.start()] + content[m.end():]
    return content

html_content = remove_func('calc', html_content)
html_content = remove_func('ubdg', html_content)

# Fix SVG internal coordinate mapping to map 1:1 to physical pixels
old_rv = r'const svgW=parseFloat(vb[2]),svgH=parseFloat(vb[3]);'
new_rv = r"const svgW=parseFloat(vb[2]),svgH=parseFloat(vb[3]);svg.style.width=svgW+'px';svg.style.height=svgH+'px';"
html_content = html_content.replace(old_rv, new_rv)

# Adjust the map default view to center exactly on the cluster of plots (x=1200, y=1000)
old_rv2 = r'sc=fitScale;px=(r.width-svgW*fitScale)/2;py=(r.height-svgH*fitScale)/2;at();'
new_rv2 = r'sc=fitScale*2.5; px=r.width/2 - 1200*sc; py=r.height/2 - 1000*sc; at();'
html_content = html_content.replace(old_rv2, new_rv2)

with open(os.path.join(app_dir, 'wix_map.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

print("wix_map.html generated successfully!")
