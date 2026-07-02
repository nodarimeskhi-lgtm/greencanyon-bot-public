import os

base_dir = r"c:\Users\Nodar\2026 antigraviti"
extensions = ['.geojson', '.kml', '.dxf', '.dwg', '.shp', '.svg', '.json']

found = []
for root, dirs, files in os.walk(base_dir):
    if any(x in root for x in [".git", "node_modules", ".agent", ".vscode"]):
        continue
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in extensions:
            path = os.path.join(root, file)
            found.append((path, os.path.getsize(path)))

print(f"Found {len(found)} vector/geometry/JSON files:")
for p, s in sorted(found, key=lambda x: x[1], reverse=True):
    print(f"  {p} ({s/1024:.1f} KB)")
