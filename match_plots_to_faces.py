import re
import os
import json
import xml.etree.ElementTree as ET
import math

svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"
plot_pos_path = r"c:\Users\Nodar\2026 antigraviti\plot_positions.json"

if not os.path.exists(svg_path) or not os.path.exists(plot_pos_path):
    print("Files missing")
    exit(1)

with open(plot_pos_path, 'r', encoding='utf-8') as f:
    plot_positions = json.load(f)

# Re-use parser
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
                if cmd_char == 'h':
                    curr[0] += x
                else:
                    curr[0] = x
                points.append(tuple(curr))
            elif cmd_char in ['V', 'v']:
                y = float(tokens[i][1])
                i += 1
                if cmd_char == 'v':
                    curr[1] += y
                else:
                    curr[1] = y
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

tree = ET.parse(svg_path)
root = tree.getroot()

ns = {'svg': 'http://www.w3.org/2000/svg'}
paths = root.findall('.//svg:path', ns)
if not paths:
    paths = root.findall('.//path')

segments = []
for idx, p in enumerate(paths):
    d = p.attrib.get('d', '')
    if not d:
        continue
    transform = p.attrib.get('transform', '')
    try:
        pts = parse_path_d(d)
        if len(pts) == 2:
            if transform and 'matrix' in transform:
                match = re.search(r'matrix\(([^)]+)\)', transform)
                if match:
                    vals = [float(x.strip()) for x in match.group(1).split(',')]
                    if len(vals) == 6:
                        a, b, c_val, d_val, e, f = vals
                        t_pts = []
                        for px, py in pts:
                            tx = a * px + c_val * py + e
                            ty = b * px + d_val * py + f
                            t_pts.append((tx, ty))
                        pts = t_pts
            segments.append((pts[0], pts[1]))
    except:
        pass

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

# Calculate centroids of all faces
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

# Map plots to these polygons
# Note: plot_positions coordinates x and y are relative offsets from the center of the SVG
# Center is centerX: 841.9, centerY: 1192.0
# So plot_position coordinates are px_svg = centerX + x, py_svg = centerY + y
# Wait, let's verify if the SVG Y coordinate is flipped?
# Look at the SVG path: matrix(1, 0, 0, -1, 1191.97, 841.89) has -1 for Y scale!
# Flipped Y is common. Let's check both flipped and unflipped Y to find the best match!

centerX = 841.9
centerY = 1192.0

matches_normal = {}
matches_flipped_y = {}

for pid, pos in plot_positions.items():
    px_normal = centerX + pos['x']
    py_normal = centerY + pos['y']
    
    # Flipped Y
    px_flipped = centerX + pos['x']
    py_flipped = centerY - pos['y'] # flipped Y offset
    
    # Find closest normal
    best_norm = None
    min_dist_norm = 999999.0
    for poly in reconstructed_polys:
        d_val = dist((poly['cx'], poly['cy']), (px_normal, py_normal))
        if d_val < min_dist_norm:
            min_dist_norm = d_val
            best_norm = poly
            
    # Find closest flipped Y
    best_flip = None
    min_dist_flip = 999999.0
    for poly in reconstructed_polys:
        d_val = dist((poly['cx'], poly['cy']), (px_flipped, py_flipped))
        if d_val < min_dist_flip:
            min_dist_flip = d_val
            best_flip = poly
            
    matches_normal[pid] = (best_norm, min_dist_norm)
    matches_flipped_y[pid] = (best_flip, min_dist_flip)

# Print average distance for both mapping strategies
avg_dist_normal = sum(m[1] for m in matches_normal.values()) / len(plot_positions)
avg_dist_flipped = sum(m[1] for m in matches_flipped_y.values()) / len(plot_positions)

print(f"Average match distance (Normal Y): {avg_dist_normal:.2f} pixels")
print(f"Average match distance (Flipped Y): {avg_dist_flipped:.2f} pixels")

# Let's inspect some sample matches for the best strategy
best_strategy = matches_normal if avg_dist_normal < avg_dist_flipped else matches_flipped_y
strategy_name = "Normal Y" if avg_dist_normal < avg_dist_flipped else "Flipped Y"
print(f"\nUsing {strategy_name} strategy:")

sample_ids = ["LA-3", "LA-15", "LB-2", "LC-10"]
for pid in sample_ids:
    if pid in best_strategy:
        poly, d_val = best_strategy[pid]
        print(f"  {pid}: match distance = {d_val:.2f} px, vertices count = {len(poly['points'])}")
        # print first few points
        print(f"    Points: {poly['points']}")
