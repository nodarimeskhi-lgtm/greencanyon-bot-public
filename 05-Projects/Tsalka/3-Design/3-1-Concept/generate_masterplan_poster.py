"""
Tsalka Masterplan Poster -- Alpine Cartography
Generates a design-forward architectural masterplan visualization.
"""

import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

random.seed(42)

W, H = 2400, 3200
FONTS_DIR = Path(r"x:\Galt\.cursor\skills\canvas-design\canvas-fonts")
OUTPUT = Path(r"x:\Galt\05-Projects\Tsalka\3-Design\3-1-Concept\Tsalka_Masterplan_Poster.png")

BG = (245, 243, 238)
FOREST_DEEP = (34, 62, 41)
FOREST_MID = (52, 88, 58)
MEADOW = (142, 163, 108)
MEADOW_LIGHT = (188, 198, 156)
FIELD_GOLD = (198, 186, 140)
STONE_WARM = (168, 148, 120)
STONE_LIGHT = (198, 182, 158)
PATH_COLOR = (178, 168, 148)
WATER = (108, 138, 158)
TEXT_DARK = (42, 42, 38)
TEXT_LIGHT = (128, 122, 108)
ACCENT = (162, 88, 52)
CONTOUR = (168, 162, 148)
GRID_COLOR = (218, 214, 206)


def load_font(name, size):
    try:
        return ImageFont.truetype(str(FONTS_DIR / name), size)
    except Exception:
        return ImageFont.load_default()


font_title = load_font("BigShoulders-Regular.ttf", 72)
font_subtitle = load_font("WorkSans-Italic.ttf", 28)
font_label = load_font("IBMPlexMono-Regular.ttf", 16)
font_label_bold = load_font("IBMPlexMono-Bold.ttf", 16)
font_tiny = load_font("IBMPlexMono-Regular.ttf", 12)
font_number = load_font("DMMono-Regular.ttf", 14)
font_section = load_font("WorkSans-Bold.ttf", 22)
font_note = load_font("InstrumentSerif-Italic.ttf", 18)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)


def draw_contour_lines(draw, cx, cy, radius, rings, color, width=1):
    for i in range(rings):
        r = radius - i * (radius // rings)
        offset_x = random.uniform(-3, 3)
        offset_y = random.uniform(-3, 3)
        points = []
        for angle in range(0, 361, 3):
            rad = math.radians(angle)
            noise = random.uniform(-r * 0.04, r * 0.04)
            x = cx + offset_x + (r + noise) * math.cos(rad)
            y = cy + offset_y + (r + noise) * 0.6 * math.sin(rad)
            points.append((x, y))
        if len(points) > 2:
            alpha = max(40, 255 - i * 25)
            c = tuple(int(cc * alpha / 255 + BG[j] * (255 - alpha) / 255) for j, cc in enumerate(color))
            draw.line(points, fill=c, width=width)


for y_offset in range(0, H, 80):
    draw.line([(0, y_offset), (W, y_offset)], fill=GRID_COLOR, width=1)
for x_offset in range(0, W, 80):
    draw.line([(x_offset, 0), (x_offset, H)], fill=GRID_COLOR, width=1)


draw_contour_lines(draw, 600, 1200, 800, 18, CONTOUR, 1)
draw_contour_lines(draw, 1600, 1800, 600, 14, CONTOUR, 1)
draw_contour_lines(draw, 1000, 2200, 500, 12, CONTOUR, 1)


def draw_organic_shape(draw, cx, cy, w, h, color, irregularity=0.08):
    points = []
    for angle in range(0, 360, 5):
        rad = math.radians(angle)
        noise = random.uniform(-irregularity, irregularity)
        x = cx + (w / 2) * (1 + noise) * math.cos(rad)
        y = cy + (h / 2) * (1 + noise) * math.sin(rad)
        points.append((x, y))
    draw.polygon(points, fill=color)


draw_organic_shape(draw, 350, 1100, 500, 700, FOREST_DEEP, 0.12)
draw_organic_shape(draw, 420, 1300, 400, 500, FOREST_MID, 0.10)
draw_organic_shape(draw, 250, 900, 350, 400, FOREST_MID, 0.10)

draw_organic_shape(draw, 550, 1800, 700, 400, FOREST_DEEP, 0.10)
draw_organic_shape(draw, 400, 2000, 500, 350, FOREST_MID, 0.08)

draw_organic_shape(draw, 1500, 900, 600, 300, MEADOW, 0.06)
draw_organic_shape(draw, 1700, 1100, 500, 250, MEADOW_LIGHT, 0.06)
draw_organic_shape(draw, 1900, 1500, 400, 600, FIELD_GOLD, 0.05)


road_points = []
for t in range(100):
    x = 200 + t * 20 + math.sin(t * 0.15) * 60
    y = 600 + t * 22 + math.cos(t * 0.1) * 40
    road_points.append((x, y))

for offset in [-6, -5, 5, 6]:
    shifted = [(x, y + offset) for x, y in road_points]
    draw.line(shifted, fill=PATH_COLOR, width=2)
draw.line(road_points, fill=STONE_LIGHT, width=8)


cottage_positions = []
base_x, base_y = 850, 1050
for row in range(8):
    count = 6 + (row % 3)
    for col in range(count):
        cx = base_x + col * 85 + (row % 2) * 40 + random.uniform(-8, 8)
        cy = base_y + row * 90 + random.uniform(-5, 5)
        if cx < W - 200 and cy < 2100:
            cottage_positions.append((cx, cy))

for cx, cy in cottage_positions:
    w = random.choice([28, 32, 36])
    h = random.choice([22, 26, 28])
    angle = random.uniform(-5, 5)
    shadow_offset = 3
    draw.rectangle([cx + shadow_offset, cy + shadow_offset, cx + w + shadow_offset, cy + h + shadow_offset],
                   fill=(200, 195, 185))
    draw.rectangle([cx, cy, cx + w, cy + h], fill=STONE_WARM, outline=TEXT_DARK, width=1)
    roof_h = 6
    draw.polygon([(cx - 2, cy), (cx + w / 2, cy - roof_h), (cx + w + 2, cy)], fill=(148, 128, 100))


community_buildings = [
    (950, 950, 80, 50, "HOTEL"),
    (1100, 980, 60, 40, "SPA"),
    (850, 960, 55, 35, "RESTAURANT"),
    (1050, 1050, 45, 30, "RECEPTION"),
]

for bx, by, bw, bh, name in community_buildings:
    draw.rectangle([bx + 4, by + 4, bx + bw + 4, by + bh + 4], fill=(190, 185, 175))
    draw.rectangle([bx, by, bx + bw, by + bh], fill=ACCENT, outline=TEXT_DARK, width=2)
    bbox = draw.textbbox((0, 0), name, font=font_tiny)
    tw = bbox[2] - bbox[0]
    draw.text((bx + bw / 2 - tw / 2, by + bh + 6), name, fill=TEXT_DARK, font=font_tiny)

farm_x, farm_y = 1600, 1600
draw.rectangle([farm_x, farm_y, farm_x + 100, farm_y + 60], fill=(108, 128, 88), outline=TEXT_DARK, width=2)
draw.rectangle([farm_x + 120, farm_y + 10, farm_x + 180, farm_y + 50], fill=(128, 148, 98), outline=TEXT_DARK, width=1)
draw.rectangle([farm_x - 60, farm_y + 10, farm_x - 10, farm_y + 50], fill=(118, 138, 88), outline=TEXT_DARK, width=1)
draw.text((farm_x + 10, farm_y + 65), "ECO-FARM", fill=TEXT_DARK, font=font_label)

for gx in range(farm_x + 200, farm_x + 500, 70):
    draw.rectangle([gx, farm_y - 20, gx + 55, farm_y + 25], fill=(168, 188, 148), outline=(98, 118, 78), width=1)
draw.text((farm_x + 220, farm_y + 30), "GREENHOUSES", fill=TEXT_DARK, font=font_tiny)


stable_x, stable_y = 1650, 1750
draw.rectangle([stable_x, stable_y, stable_x + 70, stable_y + 40], fill=(148, 128, 98), outline=TEXT_DARK, width=1)
draw.ellipse([stable_x + 80, stable_y - 10, stable_x + 220, stable_y + 50], outline=STONE_WARM, width=2)
draw.text((stable_x + 5, stable_y + 45), "STABLES & ARENA", fill=TEXT_DARK, font=font_tiny)


for i in range(20):
    tx = random.uniform(200, 700)
    ty = random.uniform(1000, 1500)
    size = random.randint(4, 10)
    draw.ellipse([tx - size, ty - size, tx + size, ty + size], fill=FOREST_DEEP)

for i in range(15):
    tx = random.uniform(800, 1400)
    ty = random.uniform(1100, 1900)
    size = random.randint(3, 7)
    draw.ellipse([tx - size, ty - size, tx + size, ty + size], fill=MEADOW)


margin = 120
draw.text((margin, 100), "TSALKA", fill=TEXT_DARK, font=font_title)
draw.text((margin, 180), "Green Canyon Alpine Village  \u00b7  Masterplan", fill=TEXT_LIGHT, font=font_subtitle)

draw.line([(margin, 230), (margin + 300, 230)], fill=ACCENT, width=2)


legend_y = 2400
draw.text((margin, legend_y - 40), "LEGEND", fill=TEXT_DARK, font=font_section)
draw.line([(margin, legend_y - 15), (margin + 80, legend_y - 15)], fill=ACCENT, width=1)

legend_items = [
    (STONE_WARM, "Residential Cottages (170 units)"),
    (ACCENT, "Community & Hospitality"),
    ((108, 128, 88), "Eco-Farm Complex"),
    ((168, 188, 148), "Greenhouses (1,500 m\u00b2)"),
    ((148, 128, 98), "Equestrian Center"),
    (FOREST_DEEP, "Preserved Forest"),
    (MEADOW, "Alpine Meadows"),
    (FIELD_GOLD, "Agricultural Fields"),
    (STONE_LIGHT, "Road Network"),
]

for i, (color, label) in enumerate(legend_items):
    ly = legend_y + i * 30
    draw.rectangle([margin, ly, margin + 18, ly + 18], fill=color, outline=TEXT_DARK, width=1)
    draw.text((margin + 28, ly + 1), label, fill=TEXT_DARK, font=font_label)


stats_x = 1400
draw.text((stats_x, legend_y - 40), "PROJECT DATA", fill=TEXT_DARK, font=font_section)
draw.line([(stats_x, legend_y - 15), (stats_x + 120, legend_y - 15)], fill=ACCENT, width=1)

stats = [
    ("TOTAL AREA", "~25 ha"),
    ("COTTAGES", "170 units"),
    ("APARTMENTS", "100 units"),
    ("CAPACITY", "~800 persons/day"),
    ("ELEVATION", "1,400\u20131,600 m"),
    ("ECO-FARM", "1.2 ha"),
    ("GREENHOUSES", "1,500 m\u00b2"),
    ("LIVESTOCK", "40 cattle, 12 horses"),
]

for i, (key, val) in enumerate(stats):
    sy = legend_y + i * 30
    draw.text((stats_x, sy + 1), key, fill=TEXT_LIGHT, font=font_label)
    draw.text((stats_x + 200, sy + 1), val, fill=TEXT_DARK, font=font_label_bold)


coord_labels = [
    (W - margin - 200, 100, "41\u00b041'N  44\u00b005'E"),
    (W - margin - 200, 130, "Tsalka Municipality, Georgia"),
]
for cx, cy, text in coord_labels:
    draw.text((cx, cy), text, fill=TEXT_LIGHT, font=font_number)


note_y = 2700
draw.text((margin, note_y), "\u201cWe are not building a hotel near a farm.", fill=TEXT_LIGHT, font=font_note)
draw.text((margin, note_y + 28), "We are creating Georgia\u2019s most developed alpine village.\u201d", fill=TEXT_LIGHT, font=font_note)

draw.line([(margin, 2800), (W - margin, 2800)], fill=CONTOUR, width=1)

draw.text((margin, 2820), "GALT Development  \u00b7  2025\u20132026", fill=TEXT_LIGHT, font=font_tiny)
draw.text((margin, 2840), "Concept Design  \u00b7  Alpine Cartography Philosophy", fill=TEXT_LIGHT, font=font_tiny)


for i in range(5):
    nx = margin + i * 200
    ny = 260
    draw.line([(nx, ny), (nx, ny + 10)], fill=TEXT_LIGHT, width=1)
    draw.text((nx + 3, ny + 12), f"{i * 100}m", fill=TEXT_LIGHT, font=font_tiny)
draw.line([(margin, 270), (margin + 800, 270)], fill=TEXT_LIGHT, width=1)

north_x, north_y = W - margin - 60, 280
draw.line([(north_x, north_y + 40), (north_x, north_y - 20)], fill=TEXT_DARK, width=2)
draw.polygon([(north_x - 8, north_y - 10), (north_x, north_y - 30), (north_x + 8, north_y - 10)], fill=TEXT_DARK)
draw.text((north_x - 4, north_y + 45), "N", fill=TEXT_DARK, font=font_label_bold)


img.save(str(OUTPUT), quality=95, dpi=(300, 300))
print(f"Poster saved to {OUTPUT}")
print(f"Size: {W}x{H}px at 300 DPI = {W/300*25.4:.0f}x{H/300*25.4:.0f}mm")
