import re
import xml.etree.ElementTree as ET

svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"

def parse_path_d(d_string):
    tokens = re.findall(r'([a-zA-Z])|([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', d_string)
    points = []
    curr = [0.0, 0.0]
    start_pt = [0.0, 0.0]
    
    i = 0
    cmd_char = ''
    while i < len(tokens):
        cmd = tokens[i][0]
        if cmd:
            cmd_char = cmd
            i += 1
        if i >= len(tokens):
            break
        try:
            if cmd_char in ['M', 'm']:
                x = float(tokens[i][1])
                y = float(tokens[i+1][1])
                i += 2
                if cmd_char == 'm': curr[0] += x; curr[1] += y
                else: curr[0] = x; curr[1] = y
                points.append(tuple(curr))
                start_pt = list(curr)
                cmd_char = 'L' if cmd_char == 'M' else 'l'
            elif cmd_char in ['L', 'l']:
                x = float(tokens[i][1])
                y = float(tokens[i+1][1])
                i += 2
                if cmd_char == 'l': curr[0] += x; curr[1] += y
                else: curr[0] = x; curr[1] = y
                points.append(tuple(curr))
            elif cmd_char in ['H', 'h']:
                x = float(tokens[i][1]); i += 1
                if cmd_char == 'h': curr[0] += x
                else: curr[0] = x
                points.append(tuple(curr))
            elif cmd_char in ['V', 'v']:
                y = float(tokens[i][1]); i += 1
                if cmd_char == 'v': curr[1] += y
                else: curr[1] = y
                points.append(tuple(curr))
            elif cmd_char in ['C', 'c']:
                args = [float(tokens[i+j][1]) for j in range(6)]; i += 6
                if cmd_char == 'c': curr[0] += args[4]; curr[1] += args[5]
                else: curr[0] = args[4]; curr[1] = args[5]
                points.append(tuple(curr))
            elif cmd_char in ['S', 's']:
                args = [float(tokens[i+j][1]) for j in range(4)]; i += 4
                if cmd_char == 's': curr[0] += args[2]; curr[1] += args[3]
                else: curr[0] = args[2]; curr[1] = args[3]
                points.append(tuple(curr))
            elif cmd_char in ['Z', 'z']:
                curr = list(start_pt)
                points.append(tuple(curr))
            else:
                i += 1
        except:
            i += 1
    return points

def parse_transform(t_str):
    if not t_str: return [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    match = re.search(r'matrix\(([^)]+)\)', t_str)
    if match:
        vals = [float(x.strip()) for x in re.split(r'[\s,]+', match.group(1).strip()) if x.strip()]
        if len(vals) == 6: return vals
    return [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]

def multiply_matrices(m1, m2):
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return [
        a1*a2 + c1*b2, b1*a2 + d1*b2,
        a1*c2 + c1*d2, b1*c2 + d1*d2,
        a1*e2 + c1*f2 + e1, b1*e2 + d1*f2 + f1
    ]

tree = ET.parse(svg_path)
root = tree.getroot()

min_x, max_x = 999999.0, -999999.0
min_y, max_y = 999999.0, -999999.0

def traverse(element, current_matrix):
    global min_x, max_x, min_y, max_y
    t_str = element.attrib.get('transform', '')
    local_m = parse_transform(t_str)
    accum_m = multiply_matrices(current_matrix, local_m)
    
    tag = element.tag.split('}')[-1]
    if tag == 'path':
        d = element.attrib.get('d', '')
        if d:
            try:
                pts = parse_path_d(d)
                a, b, c, d_val, e, f = accum_m
                for px, py in pts:
                    tx = a * px + c * py + e
                    ty = b * px + d_val * py + f
                    if tx < min_x: min_x = tx
                    if tx > max_x: max_x = tx
                    if ty < min_y: min_y = ty
                    if ty > max_y: max_y = ty
            except:
                pass
    for child in element:
        traverse(child, accum_m)

traverse(root, [1.0, 0.0, 0.0, 1.0, 0.0, 0.0])
print(f"Overall bounding box of SVG paths:")
print(f"  X range: {min_x:.2f} to {max_x:.2f} (width: {max_x-min_x:.2f})")
print(f"  Y range: {min_y:.2f} to {max_y:.2f} (height: {max_y-min_y:.2f})")
