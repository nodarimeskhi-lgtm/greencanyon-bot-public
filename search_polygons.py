import os
import re
import json

base_dir = r"c:\Users\Nodar\2026 antigraviti"

def search_files():
    found_files = []
    # Walk through the directory and look for JSON and HTML files
    for root, dirs, files in os.walk(base_dir):
        if any(x in root for x in [".git", "node_modules", ".agent", ".vscode", "Junk"]):
            continue
        for file in files:
            if file.endswith(('.json', '.html', '.js', '.txt')):
                path = os.path.join(root, file)
                try:
                    # check size to avoid reading massive files
                    size = os.path.getsize(path)
                    if size > 5 * 1024 * 1024 and not file.endswith('wix_map.html'): # skip files > 5MB except wix_map
                        continue
                    
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    # Check for polygons or arrays of coords
                    if "polygon" in content.lower() or "coords" in content.lower() or "path" in content.lower():
                        # check if it contains plot IDs
                        if any(pid in content for pid in ["LA-1", "LA-15", "LB-2", "LC-10"]):
                            found_files.append((path, size))
                except Exception as e:
                    pass
    return found_files

found = search_files()
print(f"Found {len(found)} candidate files containing polygons/coordinates and plot IDs:")
for p, s in found:
    print(f"  {p} ({s/1024:.1f} KB)")
