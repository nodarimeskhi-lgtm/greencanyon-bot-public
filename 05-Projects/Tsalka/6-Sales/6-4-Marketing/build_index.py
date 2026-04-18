import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read template
with open(r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\portal_template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Read inventory JS
with open(r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\inventory_js.txt', 'r', encoding='utf-8') as f:
    inv_js = f.read()

# Fix the ternary operator syntax error in template (| instead of |)
html = html.replace(
    "p.zone!=='AH'?' | '+p.area+'m² ნაკვ.':|' Apart Hotel')",
    "p.zone!=='AH'?' | '+p.area+'m² ნაკვ.':' Apart Hotel')"
)

# Replace placeholder
if 'INVENTORY_PLACEHOLDER' in html:
    html = html.replace('INVENTORY_PLACEHOLDER', inv_js)
    print('✅ Placeholder replaced')
else:
    print('❌ Placeholder not found!')
    sys.exit(1)

out = r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\index.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = len(html) // 1024
plot_count = html.count('{id:')
print(f'✅ index.html written — {size_kb}KB, ~{plot_count} plots')
print(f'Path: {out}')
