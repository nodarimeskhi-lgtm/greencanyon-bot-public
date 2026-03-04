import pdfplumber
import pandas as pd
import json
import re

pdf_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-5-Presentations\2026-FEB-5.pdf"

def clean_area(area_str):
    if not area_str:
        return None
    # Extract numbers and decimal point
    area_str = str(area_str).replace(",", ".")
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

# Extract data from all tables on all pages
all_plots = []
print("Opening PDF...")
with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    for i, page in enumerate(pdf.pages):
        print(f"Processing page {i+1}...")
        tables = page.extract_tables()
        print(f"Found {len(tables)} tables on page {i+1}")
        for j, table in enumerate(tables):
            print(f"  Table {j+1} has {len(table)} rows")
            for row in table:
                # Expecting row to have at least 3 columns: [Plot#, Type, Area, ...]
                if len(row) >= 3:
                    plot_num = str(row[0]).strip() if row[0] else ""
                    type_mark = str(row[1]).strip() if row[1] else ""
                    area_str = str(row[2]).strip() if row[2] else ""
                    
                    # Check if it's a plot: plot_num should be a number (mostly)
                    # and type_mark should be LA, LB, LC, LD
                    if plot_num and plot_num.replace(".","").isdigit() and type_mark in ["LA", "LB", "LC", "LD"]:
                        all_plots.append({
                            "ნაკვეთი #": plot_num,
                            "ტიპი": type_mark,
                            "ნაკვეთის ფართობი": area_str
                        })
print(f"Extracted {len(all_plots)} potential plots.")

# Create DataFrame
df = pd.DataFrame(all_plots)

# Identify unique plots by (Plot#, Type) to avoid overlaps if tables repeat headers or such
df = df.drop_duplicates(subset=["ნაკვეთი #", "ტიპი"])

# Process data
df["ფართობი_რიცხვი"] = df["ნაკვეთის ფართობი"].apply(clean_area)
df["კოტეჯის ზომა"] = df["ფართობი_რიცხვი"].apply(get_cottage_size)

# Sort for better readability
df = df.sort_values(by=["ტიპი", "ნაკვეთი #"])

# Select and rename columns for final report
final_df = df[["ნაკვეთი #", "ტიპი", "ნაკვეთის ფართობი", "კოტეჯის ზომა"]]

# Save to Excel
output_path = r"C:\Users\Nodar\2026 antigraviti\კოტეჯების_ზომები_სრული.xlsx"
final_df.to_excel(output_path, index=False)

# Calculate summary
counts = final_df["კოტეჯის ზომა"].value_counts().to_dict()
total_plots = len(final_df)

# Save summary to file
summary = {
    "file_path": output_path,
    "counts": counts,
    "total_plots": total_plots
}
with open(r"C:\Users\Nodar\2026 antigraviti\summary_full.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=4)
