import re
import os

wix_app_path = r"c:\Users\Nodar\2026 antigraviti\Wix_Final_App\index.html"

with open(wix_app_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's find <g> tags and see what's inside
# Find all <g> blocks in the SVG
g_blocks = re.findall(r'<g[^>]*>.*?</g>', content, flags=re.DOTALL)
print(f"Total <g> blocks: {len(g_blocks)}")

# Let's filter groups that contain text or circles
plot_groups = []
for g in g_blocks:
    if "LA-15" in g or "cx=" in g or "data-id=" in g:
        plot_groups.append(g)

print(f"Groups containing plot info: {len(plot_groups)}")
for idx, g in enumerate(plot_groups[:5]):
    print(f"\nGroup {idx}:")
    print(g[:500] + ("..." if len(g) > 500 else ""))
