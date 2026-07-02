import re

wix_map_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\wix_map.html"
svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"

# Read first 1000 characters of CAD SVG
with open(svg_path, 'r', encoding='utf-8') as f:
    svg_start = f.read(1500)
    print("--- CAD SVG Start ---")
    print(svg_start)

# Read root SVG tag from wix_map.html
with open(wix_map_path, 'r', encoding='utf-8') as f:
    wix_content = f.read()
    match = re.search(r'<svg[^>]*>', wix_content)
    if match:
        print("\n--- Wix Map SVG tag ---")
        print(match.group(0))
    else:
        print("\nNo SVG tag found in wix_map.html")
