import openpyxl
import os
import sys

# Ensure UTF-8 printing in Windows console if possible, or just write to file
output_file = r"c:\Users\Nodar\2026 antigraviti\scratch\act_excel_dump.txt"
f = r"c:\Users\Nodar\2026 antigraviti\ფართების_განაწილების_აქტი.xlsx"

wb = openpyxl.load_workbook(f, data_only=True)
ws = wb.active

with open(output_file, "w", encoding="utf-8") as out:
    out.write(f"Reading all rows in {f}...\n")
    for row in ws.iter_rows(values_only=True):
        if any(row):
            out.write(" | ".join([str(x) if x is not None else "" for x in row]) + "\n")

print("Done writing act_excel_dump.txt")
