import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\index.html', encoding='utf-8') as f:
    content = f.read()
checks = [
    ('I18N translation object', 'const I18N = {'),
    ('setLang querySelectorAll', 'querySelectorAll'),
    ('CORS proxy allorigins', 'allorigins.win'),
    ('Zone name', '\u10e2\u10e7\u10d8\u10e1 \u10d9\u10d5\u10d0\u10e0\u10e2\u10d0\u10da\u10d8'),
    ('data-i18n on tab', 'data-i18n="tab_map"'),
    ('fetchCSV function', 'async function fetchCSV'),
]
print()
all_ok = True
for name, marker in checks:
    found = marker in content
    if not found: all_ok = False
    print(f'  {"OK" if found else "MISSING"} | {name}')
print()
print('Build:', 'ALL FIXES IN HTML' if all_ok else 'SOME FIXES MISSING')
