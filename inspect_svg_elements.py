import re
import os
from collections import Counter

svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"

with open(svg_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print("SVG character count:", len(content))

tags = re.findall(r'<([a-zA-Z0-9:]+)', content)
c = Counter(tags)
print("\nXML tags in SVG:")
for tag, count in c.most_common(20):
    print(f"  <{tag}>: {count}")
    
# Let's see if there are any paths with coordinates or ids
paths_with_id = re.findall(r'<path[^>]*id=["\']([^"\']+)["\']', content)
print(f"\nPaths with ID: {len(paths_with_id)}")
if paths_with_id:
    print("Sample path IDs:", paths_with_id[:20])
    
# Check paths without ID
all_paths = re.findall(r'<path[^>]*>', content)
print(f"Total paths: {len(all_paths)}")

# Check groups
all_gs = re.findall(r'<g[^>]*>', content)
print(f"Total groups: {len(all_gs)}")
for idx, g in enumerate(all_gs[:15]):
    print(f"  G {idx}: {g[:150]}")
