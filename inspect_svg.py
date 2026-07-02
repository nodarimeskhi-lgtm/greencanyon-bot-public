import re
import os

svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"
wix_map_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\wix_map.html"

print("--- SVG ---")
if os.path.exists(svg_path):
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print("Found LA- in SVG:", "LA-" in content)
    print("Found 'id=' in SVG:", "id=" in content)
    # print some ids if found
    all_ids = re.findall(r'id=["\']([^"\']+)["\']', content)
    print(f"Total IDs: {len(all_ids)}")
    print("Sample IDs:", all_ids[:20])
else:
    print("SVG not found")

print("\n--- wix_map.html ---")
if os.path.exists(wix_map_path):
    with open(wix_map_path, 'r', encoding='utf-8') as f:
        # read first 1000000 chars or search line by line
        found = []
        for line in f:
            if 'LA-15' in line:
                found.append(line.strip()[:200])
                if len(found) > 5:
                    break
        print(f"Found 'LA-15' occurrences in wix_map.html: {len(found)}")
        for idx, fline in enumerate(found):
            print(f"  {idx}: {fline}")
else:
    print("wix_map.html not found")
