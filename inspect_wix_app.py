import re
import os

wix_app_path = r"c:\Users\Nodar\2026 antigraviti\Wix_Final_App\index.html"

if os.path.exists(wix_app_path):
    with open(wix_app_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    print("Found LA- in Wix_Final_App/index.html:", "LA-" in content)
    
    # Search for polygons or paths with plot IDs
    paths = re.findall(r'<path[^>]*id=["\'](L[A-D]-\d+)["\'][^>]*d=["\']([^"\']+)["\']', content)
    print(f"Found {len(paths)} <path> elements with plot IDs.")
    if paths:
        for pid, d in paths[:5]:
            print(f"  {pid}: d='{d[:100]}...'")
            
    polygons = re.findall(r'<polygon[^>]*id=["\'](L[A-D]-\d+)["\'][^>]*points=["\']([^"\']+)["\']', content)
    print(f"Found {len(polygons)} <polygon> elements with plot IDs.")
    if polygons:
        for pid, pts in polygons[:5]:
            print(f"  {pid}: points='{pts[:100]}...'")
            
    # Search for <path> or <polygon> with data-id or class
    data_paths = re.findall(r'<path[^>]*data-id=["\'](L[A-D]-\d+)["\']', content)
    print(f"Found {len(data_paths)} data-id paths.")
    
    # Print a snippet of the SVG element matching a plot ID
    match = re.search(r'(<path[^>]*id=["\']LA-15["\'][^>]*>)', content)
    if match:
        print("LA-15 path element:", match.group(1)[:300])
    match_poly = re.search(r'(<polygon[^>]*id=["\']LA-15["\'][^>]*>)', content)
    if match_poly:
        print("LA-15 polygon element:", match_poly.group(1)[:300])
        
    # Search for any tag containing a plot ID and coordinate-like strings
    match_any = re.search(r'(<[^>]+id=["\']LA-15["\'][^>]*>)', content)
    if match_any:
        print("Any LA-15 element:", match_any.group(1)[:350])
else:
    print("Wix_Final_App/index.html not found")
