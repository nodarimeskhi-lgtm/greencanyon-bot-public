import pdfplumber
import pandas as pd
import json
import re

pdf_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-5-Presentations\2026-FEB-5.pdf"

def clean_area(area_str):
    if not area_str:
        return None
    # Extract numbers and decimal point
    area_str = area_str.replace(",", ".")
    match = re.search(r"(\d+\.?\d*)", area_str)
    if match:
        return float(match.group(1))
    return None

def get_cottage_size(area):
    if area is None:
        return None
    if area < 400:
        return "65 მ2"
    elif 400 <= area <= 600:
        return "120 მ2"
    else:
        return "180 მ2"

# Extract data
with pdfplumber.open(pdf_path) as pdf:
    all_rows = []
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            # Filter out header rows if they repeat or are null
            for row in table:
                if row[0] and row[0].isdigit():
                    all_rows.append(row)

# Create DataFrame
df = pd.DataFrame(all_rows, columns=["ნაკვეთი #", "ტიპი", "ნაკვეთის ფართობი", "ზონა"])

# Process data
df["ფართობი_რიცხვი"] = df["ნაკვეთის ფართობი"].apply(clean_area)
df["კოტეჯის ზომა"] = df["ფართობი_რიცხვი"].apply(get_cottage_size)

# Select and rename columns for final report
final_df = df[["ნაკვეთი #", "ნაკვეთის ფართობი", "კოტეჯის ზომა"]]

# Save to Excel
output_path = r"C:\Users\Nodar\2026 antigraviti\კოტეჯების_ზომები.xlsx"
final_df.to_excel(output_path, index=False)

# Calculate summary
counts = final_df["კოტეჯის ზომა"].value_counts().to_dict()

# Save summary to file to avoid console encoding issues
summary = {
    "file_path": output_path,
    "counts": counts
}
with open(r"C:\Users\Nodar\2026 antigraviti\summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=4)
