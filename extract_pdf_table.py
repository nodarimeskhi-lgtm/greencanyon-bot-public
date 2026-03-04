import pdfplumber
import pandas as pd
import json

pdf_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-5-Presentations\2026-FEB-5.pdf"

with pdfplumber.open(pdf_path) as pdf:
    all_rows = []
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            all_rows.extend(table)

# Print as JSON for easy parsing by the model
print(json.dumps(all_rows, ensure_ascii=False))
