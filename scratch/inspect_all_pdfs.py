import pdfplumber
import os

folder = r"c:\Users\Nodar\Batumi Hills"
pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]

output_file = r"c:\Users\Nodar\2026 antigraviti\scratch\extracts_inspect.txt"

with open(output_file, "w", encoding="utf-8") as out:
    for file in pdf_files:
        path = os.path.join(folder, file)
        out.write(f"\n=================== {file} (Size: {os.path.getsize(path)} bytes) ===================\n")
        try:
            with pdfplumber.open(path) as pdf:
                # Read page 1
                page = pdf.pages[0]
                text = page.extract_text()
                out.write("--- Page 1 ---\n")
                if text:
                    out.write(text[:1500]) # First 1500 chars of page 1
                else:
                    out.write("[No text extracted]\n")
                
                # If there are more pages, check if "ამონაწერი" is in the text
                out.write(f"\nTotal pages: {len(pdf.pages)}\n")
        except Exception as e:
            out.write(f"Error: {e}\n")

print("Done! Written to extracts_inspect.txt")
