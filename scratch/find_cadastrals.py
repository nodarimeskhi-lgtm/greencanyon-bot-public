import re

with open(r"c:\Users\Nodar\2026 antigraviti\scratch\pdf_text_dump.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Find all occurrences of cadastral code patterns like 05.26.32.118.xx.xx.xxx
pattern = r"05\.26\.32\.118\.\d{2}\.\d{2}\.\d{3}"
matches = re.findall(pattern, text)
unique_matches = sorted(list(set(matches)))

print(f"Found {len(matches)} matches, {len(unique_matches)} unique:")
for m in unique_matches:
    print(m)
