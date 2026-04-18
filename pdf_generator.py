import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Paths
source_file = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\Land_Plot_and_Cottage_Pricing.md"
output_pdf = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\1-Management\1-3-Budget\Land_Plot_and_Cottage_Pricing.pdf"

# Register Georgian Font (Sylfaen is common on Windows)
font_path = r"C:\Windows\Fonts\sylfaen.ttf"
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont('Sylfaen', font_path))
    main_font = 'Sylfaen'
else:
    main_font = 'Helvetica'

def generate_pdf():
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom Georgian Style
    geo_style = ParagraphStyle(
        'GeorgianStyle',
        parent=styles['Normal'],
        fontName=main_font,
        fontSize=10,
        leading=12
    )
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontName=main_font,
        fontSize=16,
        leading=20,
        alignment=1 # Center
    )

    elements = []

    # Content to add
    content = [
        ("PROJECT: GREEN CANYON ECO VILLAGE & RESORT", title_style),
        ("LAND PLOT & COTTAGE PRICING LIST", geo_style),
        ("-" * 50, geo_style),
    ]

    for text, style in content:
        elements.append(Paragraph(text, style))
        elements.append(Spacer(1, 12))

    # Table Data
    data = [
        ['ნაკვეთი', 'ფართი (მ2)', 'კოტეჯი', 'კოტეჯი ($)', 'მიწა ($)', 'ჯამი ($)'],
        ['LA-1', '702.4', 'Comfort Chalet', '264,000', '35,120', '299,000'],
        ['LA-2', '654.9', 'Comfort Chalet', '264,000', '32,745', '297,000'],
        ['LA-3', '683.2', 'Comfort Chalet', '264,000', '34,160', '298,000'],
        ['LA-4', '509.5', 'Eco Cottage', '187,000', '25,475', '212,500'],
        ['LA-5', '635.8', 'Comfort Chalet', '264,000', '31,790', '296,000'],
        ['LA-6', '491.7', 'Eco Cottage', '187,000', '24,585', '212,000'],
        ['LA-7', '561.5', 'Eco Cottage', '187,000', '28,075', '215,000'],
        ['LA-8', '557.8', 'Eco Cottage', '187,000', '27,890', '215,000'],
        ['LA-9', '740.3', 'Comfort Chalet', '264,000', '37,015', '301,000'],
        ['LA-10', '591.5', 'Eco Cottage', '187,000', '29,575', '217,000'],
        ['LA-11', '953.6', 'LUX Grand Villa', '440,000', '47,680', '488,000'],
        ['LA-15', '410.8', 'Alpine 1 Bed', '105,000', '20,540', '126,000'],
        ['LA-24', '377.7', 'Alpine Studio', '77,000', '18,885', '96,000'],
        ['LA-28', '283.2', 'Alpine Studio', '77,000', '14,160', '92,000'],
    ]

    t = Table(data, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), main_font),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(t)
    elements.append(Spacer(1, 24))
    elements.append(Paragraph("შენიშვნა: ფასები მოიცავს სრულ რემონტსა და ავეჯს.", geo_style))

    doc.build(elements)
    print(f"PDF generated: {output_pdf}")

if __name__ == "__main__":
    generate_pdf()
