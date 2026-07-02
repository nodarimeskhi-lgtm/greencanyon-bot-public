import xml.etree.ElementTree as ET
import os

svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"

tree = ET.parse(svg_path)
root = tree.getroot()

ns = {'svg': 'http://www.w3.org/2000/svg'}
paths = root.findall('.//svg:path', ns)
if not paths:
    paths = root.findall('.//path')

print(f"Total paths: {len(paths)}")

# Print details of the first 30 paths to understand their patterns
for idx, p in enumerate(paths[:30]):
    d = p.attrib.get('d', '')
    transform = p.attrib.get('transform', '')
    style = p.attrib.get('style', '')
    print(f"\nPath {idx}:")
    print(f"  d: {d[:150]}...")
    if transform:
        print(f"  transform: {transform}")
    if style:
        print(f"  style: {style[:100]}")
