import pdfplumber
import pandas as pd
import json

pdf_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\2025PRV05TGGM_13_MARCH_2026.pdf"
output_csv = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\new_unprocessed_inventory.csv"

all_data = []

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        # Read a few pages to see table structure
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                print(f"--- Page {i+1} ---")
                # print the first table on this page
                for table in tables:
                    for row in table:
                        # Clean up row items
                        cleaned_row = [str(item).replace('\n', ' ').strip() if item else "" for item in row]
                        # Only keep rows that have some content
                        if any(cleaned_row):
                            all_data.append(cleaned_row)
                            
        # Print a sample of the extracted data
        print("\nSAMPLE EXTRACTED ROWS:")
        for row in all_data[:15]:
            print(row)
            
        print("\nDATA LENGTH:", len(all_data))
        
        # We'll save it to a CSV to inspect manually if needed
        df = pd.DataFrame(all_data)
        df.to_csv(output_csv, index=False, header=False, encoding='utf-8')
        print(f"\nSaved raw extracted tables to {output_csv}")
except Exception as e:
    print(f"Error reading PDF: {e}")
