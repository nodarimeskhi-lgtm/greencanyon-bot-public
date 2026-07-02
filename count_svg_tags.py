import re
import os
from collections import Counter

wix_app_path = r"c:\Users\Nodar\2026 antigraviti\Wix_Final_App\index.html"
wix_map_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\wix_map.html"

def analyze_html(path):
    if not os.path.exists(path):
        print(f"{path} not found")
        return
    print(f"\n--- Analyzing {path} ---")
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    tags = re.findall(r'<([a-zA-Z0-9:]+)', content)
    c = Counter(tags)
    print("Top HTML/SVG tags:")
    for tag, count in c.most_common(20):
        print(f"  <{tag}>: {count}")
        
    # Check if there are paths/polygons with ids
    paths_with_id = re.findall(r'<path[^>]*id=["\']([^"\']+)["\']', content)
    print(f"Paths with ID: {len(paths_with_id)}")
    if paths_with_id:
        print("Sample path IDs:", paths_with_id[:10])
        
    polys_with_id = re.findall(r'<polygon[^>]*id=["\']([^"\']+)["\']', content)
    print(f"Polygons with ID: {len(polys_with_id)}")
    if polys_with_id:
        print("Sample polygon IDs:", polys_with_id[:10])

analyze_html(wix_app_path)
analyze_html(wix_map_path)
