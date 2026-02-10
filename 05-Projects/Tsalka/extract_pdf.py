from pypdf import PdfReader
import sys

try:
    reader = PdfReader("Green-Canyon-Eco-Village-Vash-chastnyj-gornyj-oazis.pdf")
    text = ""
    for i, page in enumerate(reader.pages):
        text += f"--- Page {i+1} ---\n"
        text += page.extract_text() + "\n"
        
    with open("extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    print("Text extracted to extracted_text.txt")
except Exception as e:
    print(f"Error: {e}")
