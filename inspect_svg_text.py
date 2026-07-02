import xml.etree.ElementTree as ET
import os
import re

svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"

if not os.path.exists(svg_path):
    print("SVG not found")
    exit(1)

# Let's read the file and look for <g> groups or text elements containing "LA-"
print("Reading SVG...")
with open(svg_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's search for "LA-15" with regular expressions to find its context
# Find LA-15 and print 200 chars around it
matches = [m.start() for m in re.finditer(r'LA-15', content)]
print(f"Found {len(matches)} occurrences of 'LA-15' in SVG:")
for i, idx in enumerate(matches):
    start = max(0, idx - 150)
    end = min(len(content), idx + 150)
    print(f"Match {i}: ... {content[start:end]} ...")

# Let's look for any "LA-" or "LB-" text to see what format it takes
text_matches = re.findall(r'<text[^>]*>(.*?)</text>', content)
print(f"Found {len(text_matches)} text elements in SVG.")
plot_texts = [t for t in text_matches if any(x in t for x in ["LA-", "LB-", "LC-", "LD-"])]
print(f"Found {len(plot_texts)} text elements containing plot prefix. Sample:", plot_texts[:10])
