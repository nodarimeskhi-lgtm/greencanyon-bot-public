from pypdf import PdfReader
import sys

try:
    reader = PdfReader(r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-5-Presentations\aghmoachine-tsalka.pdf")
    text = ""
    for i, page in enumerate(reader.pages):
        text += f"--- Page {i+1} ---\n"
        text += page.extract_text() + "\n"
        
    with open(r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\tsalka_discovery_ge_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    print("Text extracted to tsalka_discovery_ge_text.txt")
except Exception as e:
    print(f"Error: {e}")
