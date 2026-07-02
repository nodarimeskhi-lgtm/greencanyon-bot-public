import re
import os

svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"

with open(svg_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Search for group attributes like 'id', 'name', 'class', 'label'
g_tags = re.findall(r'<g([^>]+)>', content)
print(f"Total <g> tags: {len(g_tags)}")

for idx, g in enumerate(g_tags):
    # Print groups that have descriptive attributes
    if any(x in g.lower() for x in ["label", "name", "layer", "plot", "boundary", "border"]):
        print(f"Descriptive Group {idx}: {g[:200]}")
