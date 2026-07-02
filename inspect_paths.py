import re
import os

wix_app_path = r"c:\Users\Nodar\2026 antigraviti\Wix_Final_App\index.html"

with open(wix_app_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find <path> tags and see what's inside
path_tags = re.findall(r'<path[^>]*>', content)
print(f"Total <path> tags: {len(path_tags)}")

for idx, p in enumerate(path_tags[:15]):
    print(f"Path {idx}: {p[:200]}")
