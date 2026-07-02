import sys
sys.stdout.reconfigure(encoding='utf-8')
try:
    from pypdf import PdfReader
except ImportError:
    print("pypdf not found. Please install it.", file=sys.stderr)
    sys.exit(1)

def extract_text(pdf_path):
    print(f"--- Extracting from {pdf_path} ---")
    try:
        reader = PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            print(f"--- Page {i+1} ---")
            print(page.extract_text())
            print("\n")
    except Exception as e:
        print(f"Error extracting {pdf_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_text.py <pdf_path> ...")
        sys.exit(1)
    for path in sys.argv[1:]:
        extract_text(path)
