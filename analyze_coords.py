import re
import os

inventory_js_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\inventory_js.txt"

with open(inventory_js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Extract latlng values
pattern = re.compile(r"\{\s*id:\s*'([^']+)'.*?latlng:\s*\[([\d.]+)\s*,\s*([\d.]+)\]\s*\}", re.DOTALL)
plots = []
for m in pattern.finditer(js_content):
    pid = m.group(1)
    py = float(m.group(2))
    px = float(m.group(3))
    plots.append({'id': pid, 'px': px, 'py': py})

print(f"Loaded {len(plots)} plots with coordinates.")
xs = [p['px'] for p in plots]
ys = [p['py'] for p in plots]

min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
avg_x, avg_y = sum(xs)/len(xs), sum(ys)/len(ys)

print(f"Pixel X (longitude) range: {min_x:.2f} to {max_x:.2f} (width: {max_x-min_x:.2f})")
print(f"Pixel Y (latitude) range: {min_y:.2f} to {max_y:.2f} (height: {max_y-min_y:.2f})")
print(f"Centroid: X={avg_x:.2f}, Y={avg_y:.2f}")

# Group by zone and print centroids
for zone in ['LA', 'LB', 'LC', 'LD']:
    z_plots = [p for p in plots if p['id'].startswith(zone)]
    if z_plots:
        zx = sum(p['px'] for p in z_plots) / len(z_plots)
        zy = sum(p['py'] for p in z_plots) / len(z_plots)
        print(f"Zone {zone} centroid: X={zx:.2f}, Y={zy:.2f} (count: {len(z_plots)})")
