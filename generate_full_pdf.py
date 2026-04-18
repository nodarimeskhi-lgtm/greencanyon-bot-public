import pandas as pd
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Paths
csv_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\master_inventory_v2.csv"
output_pdf = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\Land_Plot_and_Cottage_Pricing_Full_Official_V2.pdf"

# Register Georgian Font
font_path = r"C:\Windows\Fonts\sylfaen.ttf"
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont('Sylfaen', font_path))
    main_font = 'Sylfaen'
else:
    main_font = 'Helvetica'

def get_cottage_type(area):
    if area >= 800:
        return "LUX Grand Villa", 440000
    elif area >= 600:
        return "Comfort Chalet", 264000
    elif area >= 450:
        return "Eco Cottage", 187000
    elif area >= 400:
        return "Alpine 1 Bed", 105000
    else:
        return "Alpine Studio", 77000

def generate_pdf():
    # Load and Clean Data
    df = pd.read_csv(csv_path)
    
    plot_list = []
    
    for _, row in df.iterrows():
        zone = row['Zone']
        num = row['Number']
        full_id = f"{zone}-{num}"
        area = row['Area_sqm']
        
        c_type, c_price = get_cottage_type(area)
        land_price = int(area * 50)
        total = c_price + land_price
        
        plot_list.append({
            'sort_zone': zone,
            'sort_num': num,
            'ნაკვეთი': full_id,
            'ფართი (მ2)': f"{area:.1f}",
            'კოტეჯი': c_type,
            'კოტეჯი ($)': f"{c_price:,}",
            'მიწა ($)': f"{land_price:,}",
            'ჯამი ($)': f"{total:,}"
        })

    # Sort Data: by Zone (LA, LB, LC, LD) and then by original number
    plot_list.sort(key=lambda x: (x['sort_zone'], x['sort_num']))
    
    # Prepare Table Data
    table_data = [['ნაკვეთი', 'ფართი (მ2)', 'კოტეჯი', 'კოტეჯი ($)', 'მიწა ($)', 'ჯამი ($)']]
    for p in plot_list:
        table_data.append([
            p['ნაკვეთი'], p['ფართი (მ2)'], p['კოტეჯი'], 
            p['კოტეჯი ($)'], p['მიწა ($)'], p['ჯამი ($)']
        ])

    # Setup PDF
    doc = SimpleDocTemplate(output_pdf, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    
    geo_style = ParagraphStyle('Geo', parent=styles['Normal'], fontName=main_font, fontSize=9, leading=11)
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontName=main_font, fontSize=14, leading=18, alignment=1)
    
    elements = []
    elements.append(Paragraph("GREEN CANYON ECO VILLAGE & RESORT", title_style))
    elements.append(Paragraph("სარეალიზაციო ინვენტარის სრული ფასწარმოქმნის ცხრილი (V2)", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"დოკუმენტი შეიცავს სრულ განახლებულ სიას: {len(plot_list)} ნაკვეთი.", geo_style))
    elements.append(Paragraph("დალაგებულია ზონების (LA, LB, LC, LD) და ნომრების მიხედვით.", geo_style))
    elements.append(Spacer(1, 12))

    t = Table(table_data, repeatRows=1, hAlign='CENTER')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), main_font),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))
    
    elements.append(t)
    doc.build(elements)
    print(f"Sorted PDF generated: {output_pdf} with {len(plot_list)} plots.")

if __name__ == "__main__":
    generate_pdf()
