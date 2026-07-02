import re

wix_map_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\wix_map.html"

with open(wix_map_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find some circles and their containing groups. We can do a simple search.
# We want to see if the circles are inside <g transform="..."> tags.
# Let's search for "LA-3" circle and print the 1000 characters before it.
pos = content.find('data-id="LA-3"')
if pos != -1:
    start = max(0, pos - 1500)
    end = pos + 500
    print("--- Context around LA-3 circle in wix_map.html ---")
    print(content[start:end])
else:
    print("Circle for LA-3 not found")
