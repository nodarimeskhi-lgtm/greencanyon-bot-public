import pdfplumber
import os

pdf_path = r"c:\Users\Nodar\Batumi Hills\BTIDB_NAPRBTI_1_2248829.pdf"
output_file = r"c:\Users\Nodar\2026 antigraviti\scratch\bti_pdf_search.txt"

with open(output_file, "w", encoding="utf-8") as out:
    if os.path.exists(pdf_path):
        out.write(f"Analyzing {pdf_path}...\n")
        try:
            with pdfplumber.open(pdf_path) as pdf:
                out.write(f"Total pages: {len(pdf.pages)}\n")
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    out.write(f"\n--- Page {i+1} ---\n")
                    if text:
                        out.write(text)
                    else:
                        out.write("[No text extracted]\n")
        except Exception as e:
            out.write(f"Error: {e}\n")
    else:
        out.write(f"Path not found: {pdf_path}\n")

print("Done searching BTI PDF!")
