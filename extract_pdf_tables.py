import pdfplumber
import pandas as pd
import os

pdf_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-5-Presentations\2026-FEB-5.pdf"
output_csv = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\full_extracted_inventory.csv"

all_data = []

try:
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                if table:
                    # Clean the table data
                    cleaned_table = []
                    for row in table:
                        if any(row): # Skip empty rows
                            cleaned_table.append([str(cell).replace('\n', ' ') if cell else '' for cell in row])
                    
                    if cleaned_table:
                        df = pd.DataFrame(cleaned_table)
                        all_data.append(df)
            print(f"Processed page {i+1}")

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        print(f"Successfully extracted {len(final_df)} rows to {output_csv}")
    else:
        print("No tables found in the PDF.")

except Exception as e:
    print(f"Error: {e}")
