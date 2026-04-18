import os
from PIL import Image, ImageDraw, ImageFont

# Dimensions for 85cm x 200cm at 150 DPI
WIDTH = 5020
HEIGHT = 11811

# Paths
BG_PATH = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\Assets\banner_bg_v4.png"
QR_PATH = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\Assets\image_48_qr.png"
OUTPUT_PNG = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\Assets\green_canyon_banner_85x200cm.png"
OUTPUT_PDF = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\Assets\green_canyon_banner_85x200cm.pdf"
FONT_DIR = r"c:\Users\Nodar\2026 antigraviti\.agent\skills\canvas-design\canvas-fonts"

def get_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

def assemble_banner():
    # 1. Create Base Canvas
    img = Image.new('RGB', (WIDTH, HEIGHT), color='black')
    draw = ImageDraw.Draw(img)

    # 2. Load and Scale Background
    if os.path.exists(BG_PATH):
        bg = Image.open(BG_PATH)
        # Calculate scaling to fill 85x200cm
        bg_w, bg_h = bg.size
        # Resize to match width, then centered crop for height
        scale = WIDTH / bg_w
        new_h = int(bg_h * scale)
        bg_scaled = bg.resize((WIDTH, new_h), Image.Resampling.LANCZOS)
        
        # If height is still smaller than required, scale by height instead
        if new_h < HEIGHT:
            scale = HEIGHT / bg_h
            new_w = int(bg_w * scale)
            bg_scaled = bg.resize((new_w, HEIGHT), Image.Resampling.LANCZOS)
            offset = (new_w - WIDTH) // 2
            img.paste(bg_scaled.crop((offset, 0, offset + WIDTH, HEIGHT)), (0, 0))
        else:
            offset = (new_h - HEIGHT) // 2
            img.paste(bg_scaled.crop((0, offset, WIDTH, offset + HEIGHT)), (0, 0))

    # 3. Add Top Text
    # "Green Canyon Eco Village" - Elegant Script
    # Using NothingYouCouldDo-Regular for script feel
    try:
        f_script = get_font("NothingYouCouldDo-Regular.ttf", 350)
        f_subtitle = get_font("InstrumentSans-Regular.ttf", 150)
        
        green_color = (26, 74, 58) # #1a4a3a
        
        # Center the text at the top
        draw.text((WIDTH // 2, 600), "Green Canyon Eco Village", font=f_script, fill=green_color, anchor="mm")
        draw.text((WIDTH // 2, 850), "Coming soon in Georgia.", font=f_subtitle, fill=green_color, anchor="mm")
    except Exception as e:
        print(f"Font loading error: {e}")

    # 4. Add QR Code (Bottom Right)
    if os.path.exists(QR_PATH):
        qr = Image.open(QR_PATH)
        qr_size = 800 # Large for print
        qr = qr.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        
        # White border square
        border = 60
        draw.rectangle([WIDTH - qr_size - 2*border - 200, HEIGHT - qr_size - 2*border - 200, 
                        WIDTH - 200, HEIGHT - 200], fill="white")
        
        img.paste(qr, (WIDTH - qr_size - border - 200, HEIGHT - qr_size - border - 200))

    # 5. Save Results
    img.save(OUTPUT_PNG, quality=95)
    img.save(OUTPUT_PDF, "PDF", resolution=150.0)
    print(f"Final Banner saved to {OUTPUT_PNG} and {OUTPUT_PDF}")

if __name__ == "__main__":
    assemble_banner()
