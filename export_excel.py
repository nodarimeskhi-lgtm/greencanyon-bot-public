import pandas as pd
import json

df = pd.read_excel('ახალი.xlsx')
# Just take the first 5 rows to understand the structure completely
data = df.head(5).to_dict(orient='records')

with open('excel_dump.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Exported excel_dump.json")
