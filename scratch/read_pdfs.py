import pdfplumber
import os
import sys

pdf_files = [
    r"c:\Users\Nodar\Batumi Hills\88202631655138578948.pdf",
    r"c:\Users\Nodar\Batumi Hills\1 pozicia 2026.pdf",
    r"c:\Users\Nodar\Batumi Hills\2 pozicia 2026.pdf",
    r"c:\Users\Nodar\Batumi Hills\3 pozicia 2027.pdf"
]

output_file = r"c:\Users\Nodar\2026 antigraviti\scratch\pdf_text_dump.txt"

with open(output_file, "w", encoding="utf-8") as out:
    for pdf_path in pdf_files:
        if os.path.exists(pdf_path):
            out.write(f"\n=================== {os.path.basename(pdf_path)} ===================\n")
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        out.write(f"--- Page {i+1} ---\n")
                        if text:
                            out.write(text)
                        else:
                            out.write("[No text extracted]\n")
            except Exception as e:
                out.write(f"Error: {e}\n")
        else:
            out.write(f"Path not found: {pdf_path}\n")

print("Done! Written to pdf_text_dump.txt")
