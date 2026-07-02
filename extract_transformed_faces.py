import re
import os
import json
import xml.etree.ElementTree as ET
import math

svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"
inventory_js_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\inventory_js.txt"

if not os.path.exists(svg_path) or not os.path.exists(inventory_js_path):
    print("Files missing")
    exit(1)

# Load plot data from inventory
plots_data = []
pattern = re.compile(r"\{\s*id:\s*'([^']+)'.*?latlng:\s*\[([\d.]+)\s*,\s*([\d.]+)\]\s*\}", re.DOTALL)
with open(inventory_js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
for m in pattern.finditer(js_content):
    plots_data.append({'id': m.group(1), 'x': float(m.group(3)), 'y': float(m.group(2))})

print(f"Loaded {len(plots_data)} plots from inventory.")

# Simple path parser (returns relative path points)
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
                if cmd_char == 'm':
                    curr[0] += x
                    curr[1] += y
                else:
                    curr[0] = x
                    curr[1] = y
                points.append(tuple(curr))
                start_pt = list(curr)
                cmd_char = 'L' if cmd_char == 'M' else 'l'
            elif cmd_char in ['L', 'l']:
                x = float(tokens[i][1])
                y = float(tokens[i+1][1])
                i += 2
                if cmd_char == 'l':
                    curr[0] += x
                    curr[1] += y
                else:
                    curr[0] = x
                    curr[1] = y
                points.append(tuple(curr))
            elif cmd_char in ['H', 'h']:
                x = float(tokens[i][1])
                i += 1
                if cmd_char == 'h': curr[0] += x
                else: curr[0] = x
                points.append(tuple(curr))
            elif cmd_char in ['V', 'v']:
                y = float(tokens[i][1])
                i += 1
                if cmd_char == 'v': curr[1] += y
                else: curr[1] = y
                points.append(tuple(curr))
            elif cmd_char in ['C', 'c']:
                args = [float(tokens[i+j][1]) for j in range(6)]
                i += 6
                if cmd_char == 'c':
                    curr[0] += args[4]
                    curr[1] += args[5]
                else:
                    curr[0] = args[4]
                    curr[1] = args[5]
                points.append(tuple(curr))
            elif cmd_char in ['S', 's']:
                args = [float(tokens[i+j][1]) for j in range(4)]
                i += 4
                if cmd_char == 's':
                    curr[0] += args[2]
                    curr[1] += args[3]
                else:
                    curr[0] = args[2]
                    curr[1] = args[3]
                points.append(tuple(curr))
            elif cmd_char in ['Z', 'z']:
                curr = list(start_pt)
                points.append(tuple(curr))
            else:
                i += 1
        except Exception as ex:
            raise ValueError(f"Error: {ex}")
    return points

# Matrix operations
def multiply_matrices(m1, m2):
    # m1, m2: [a, b, c, d, e, f] representing:
    # [a c e]
    # [b d f]
    # [0 0 1]
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
    # e.g., matrix(a, b, c, d, e, f)
    match = re.search(r'matrix\(([^)]+)\)', t_str)
    if match:
        vals = [float(x.strip()) for x in re.split(r'[\s,]+', match.group(1).strip()) if x.strip()]
        if len(vals) == 6:
            return vals
    return [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]

# Parse tree recursively to track cumulative transform matrix
tree = ET.parse(svg_path)
root = tree.getroot()

ns = {'svg': 'http://www.w3.org/2000/svg'}
segments = []

def traverse(element, current_matrix):
    # Get local transform
    t_str = element.attrib.get('transform', '')
    local_m = parse_transform(t_str)
    # Multiply
    accum_m = multiply_matrices(current_matrix, local_m)
    
    # Process path if present
    # Check if element tag is path
    tag = element.tag.split('}')[-1]
    if tag == 'path':
        d = element.attrib.get('d', '')
        if d:
            try:
                pts = parse_path_d(d)
                if len(pts) == 2:
                    a, b, c, d_val, e, f = accum_m
                    t_pts = []
                    for px, py in pts:
                        tx = a * px + c * py + e
                        ty = b * px + d_val * py + f
                        t_pts.append((tx, ty))
                    segments.append((t_pts[0], t_pts[1]))
            except:
                pass
                
    for child in element:
        traverse(child, accum_m)

# Start traversal from root
traverse(root, [1.0, 0.0, 0.0, 1.0, 0.0, 0.0])

print(f"Extracted {len(segments)} segments with cumulative transforms.")

# Build planar graph
TOL = 0.5
unique_vertices = []
def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def get_vertex(p):
    for u in unique_vertices:
        if dist(u, p) < TOL:
            return u
    unique_vertices.append(p)
    return p

std_segments = []
for s in segments:
    u = get_vertex(s[0])
    v = get_vertex(s[1])
    if u != v:
        std_segments.append((u, v))

print(f"Vertices: {len(unique_vertices)}")

adj = {u: [] for u in unique_vertices}
for u, v in std_segments:
    if v not in adj[u]: adj[u].append(v)
    if u not in adj[v]: adj[v].append(u)

edges_by_vertex = {}
for u in adj:
    edges_by_vertex[u] = sorted(adj[u], key=lambda v: math.atan2(v[1]-u[1], v[0]-u[0]))

visited_half_edges = set()
faces = []
for u in edges_by_vertex:
    for v in edges_by_vertex[u]:
        half_edge = (u, v)
        if half_edge in visited_half_edges: continue
        curr_face = [u]
        curr_u = u
        curr_v = v
        while True:
            visited_half_edges.add((curr_u, curr_v))
            curr_face.append(curr_v)
            neighbors = edges_by_vertex[curr_v]
            idx = neighbors.index(curr_u)
            next_v = neighbors[(idx + 1) % len(neighbors)]
            curr_u = curr_v
            curr_v = next_v
            if (curr_u, curr_v) == half_edge or (curr_u, curr_v) in visited_half_edges: break
        if len(curr_face) >= 4 and curr_face[0] == curr_face[-1]:
            faces.append(curr_face[:-1])

reconstructed_polys = []
for f in faces:
    cx = sum(p[0] for p in f) / len(f)
    cy = sum(p[1] for p in f) / len(f)
    reconstructed_polys.append({
        'points': f,
        'cx': cx,
        'cy': cy
    })

print(f"Reconstructed {len(reconstructed_polys)} closed polygons.")

# Match using x and y from inventory_js.txt
matches = {}
for p in plots_data:
    px = p['x']
    py = p['y']
    
    best_poly = None
    min_d = 999999.0
    for poly in reconstructed_polys:
        d_val = dist((poly['cx'], poly['cy']), (px, py))
        if d_val < min_d:
            min_d = d_val
            best_poly = poly
    matches[p['id']] = (best_poly, min_d)

avg_d = sum(m[1] for m in matches.values()) / len(plots_data)
print(f"Average match distance: {avg_d:.2f} pixels")

sample_ids = ["LA-3", "LA-15", "LB-2", "LC-10"]
for pid in sample_ids:
    if pid in matches:
        poly, d_val = matches[pid]
        print(f"  {pid}: match distance = {d_val:.2f} px, vertices count = {len(poly['points'])}")
        # print points rounded
        pts_round = [(round(x, 1), round(y, 1)) for x, y in poly['points']]
        print(f"    Points: {pts_round}")
