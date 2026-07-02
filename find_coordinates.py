import re
import os

base_dir = r"c:\Users\Nodar\2026 antigraviti"

found = []
# Match floats representing lat/lng in Tsalka Canyon range (Lat 41.5-41.7, Lng 44.0-44.2)
gps_pattern = re.compile(r'41\.\d{3,6}|44\.\d{3,6}')

for root, dirs, files in os.walk(base_dir):
    if any(x in root for x in [".git", "node_modules", ".agent", ".vscode"]):
        continue
    for file in files:
        if file.endswith(('.py', '.html', '.js', '.txt', '.md', '.json')):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                matches = gps_pattern.findall(content)
                if matches:
                    found.append((path, set(matches)))
            except:
                pass

print(f"Found GPS-like numbers in {len(found)} files:")
for p, m in found[:15]:
    print(f"  {p}: {list(m)[:10]}")
