import re
import xml.etree.ElementTree as ET

svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"

tree = ET.parse(svg_path)
root = tree.getroot()

ns = {'svg': 'http://www.w3.org/2000/svg'}

texts_found = []

# Traverse all elements to find text tags
def traverse_text(element, current_matrix):
    t_str = element.attrib.get('transform', '')
    local_m = parse_transform(t_str)
    accum_m = multiply_matrices(current_matrix, local_m)
    
    tag = element.tag.split('}')[-1]
    if tag in ['text', 'tspan']:
        txt = element.text
        if txt and ('LA-' in txt or 'LB-' in txt or 'LC-' in txt or 'LD-' in txt):
            x = float(element.attrib.get('x', 0))
            y = float(element.attrib.get('y', 0))
            # Apply matrix
            a, b, c, d_val, e, f = accum_m
            tx = a * x + c * y + e
            ty = b * x + d_val * y + f
            texts_found.append({
                'text': txt.strip(),
                'x': tx,
                'y': ty,
                'tag': tag
            })
            
    for child in element:
        traverse_text(child, accum_m)

def multiply_matrices(m1, m2):
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return [
        a1*a2 + c1*b2,
        b1*a2 + d1*b2,
        a1*c2 + c1*d2,
        b1*c2 + d1*d2,
        a1*e2 + c1*f2 + e1,
        b1*e2 + d1*f2 + f1
    ]

def parse_transform(t_str):
    if not t_str:
        return [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    match = re.search(r'matrix\(([^)]+)\)', t_str)
    if match:
        vals = [float(x.strip()) for x in re.split(r'[\s,]+', match.group(1).strip()) if x.strip()]
        if len(vals) == 6:
            return vals
    return [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]

traverse_text(root, [1.0, 0.0, 0.0, 1.0, 0.0, 0.0])

print(f"Total CAD SVG text elements with IDs found: {len(texts_found)}")
for t in texts_found[:30]:
    print(t)
