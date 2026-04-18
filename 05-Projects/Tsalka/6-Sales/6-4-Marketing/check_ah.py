import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import re

with open(r'C:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\inventory_js.txt', encoding='utf-8') as f:
    c = f.read()

ah_part = c[32000:]
print('AH-S- count:', c.count("'AH-S-"))
print('AH-JS- count:', c.count("'AH-JS-"))

# Show first 2 entries of each type
for prefix in ["AH-S-01", "AH-JS-01"]:
    idx = c.find(prefix)
    if idx > 0:
        print(f"\n--- {prefix} ---")
        print(c[idx-5:idx+220])

# Price and rent ranges
prices = [int(x) for x in re.findall(r'ah_price:(\d+)', c)]
rents = sorted(set(re.findall(r'daily_rent:(\d+)', ah_part)))
if prices:
    print(f"\nPrice range: ${min(prices):,} - ${max(prices):,}")
print(f"Daily rents used: {rents}")
