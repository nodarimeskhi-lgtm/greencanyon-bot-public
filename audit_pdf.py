import pdfplumber
import json

pdf_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-5-Presentations\2026-FEB-5.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total Pages: {len(pdf.pages)}")
    all_data = []
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        page_data = []
        for table in tables:
            page_data.append(table)
        all_data.append({
            "page": i + 1,
            "tables_found": len(tables),
            "data": page_data
        })

# Save to file to avoid console issues
with open(r"C:\Users\Nodar\2026 antigraviti\pdf_audit.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)
