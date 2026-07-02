import re
import os
import xml.etree.ElementTree as ET

wix_map_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\wix_map.html"

with open(wix_map_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the SVG block
match = re.search(r'<svg.*?>.*?</svg>', content, re.DOTALL)
if not match:
    print("No SVG block found in wix_map.html")
    exit(1)

svg_str = match.group(0)
# ET requires namespaces or ignoring them, let's parse using regex or simple parsing
print(f"SVG block size: {len(svg_str)} characters")

# Find all tags inside SVG
tags = re.findall(r'<([a-zA-Z0-9:]+)\s', svg_str)
from collections import Counter
print("Tag counts inside SVG:")
for tag, count in Counter(tags).most_common():
    print(f"  {tag}: {count}")

# Print sample circles and paths with IDs
circles_with_ids = []
paths_with_ids = []
polygons_with_ids = []

for m in re.finditer(r'<circle\s+[^>]*?data-id="([^"]+)"[^>]*?>', svg_str):
    circles_with_ids.append(m.group(0))

for m in re.finditer(r'<path\s+[^>]*?id="([^"]+)"[^>]*?>', svg_str):
    paths_with_ids.append(m.group(0))

for m in re.finditer(r'<polygon\s+[^>]*?id="([^"]+)"[^>]*?>', svg_str):
    polygons_with_ids.append(m.group(0))

print(f"\nCircles with data-id: {len(circles_with_ids)}")
print("Sample circles:")
for c in circles_with_ids[:10]:
    print("  ", c[:150])

print(f"\nPaths with id: {len(paths_with_ids)}")
print("Sample paths:")
for p in paths_with_ids[:10]:
    print("  ", p[:150])

print(f"\nPolygons with id: {len(polygons_with_ids)}")
