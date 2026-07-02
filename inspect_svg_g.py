import re
import os

svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"

with open(svg_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find <g> elements and print their opening tags
g_tags = re.findall(r'<g([^>]+)>', content)
print(f"Total groups: {len(g_tags)}")

print("\nAll groups with ID:")
count = 0
for idx, g in enumerate(g_tags):
    if "id=" in g:
        print(f"  Group {idx}: {g[:150]}")
        count += 1

print(f"Total groups with ID: {count}")
if count == 0:
    print("Wait! No groups have IDs? Let's check first 20 groups overall:")
    for idx, g in enumerate(g_tags[:20]):
        print(f"  Group {idx}: {g[:150]}")
