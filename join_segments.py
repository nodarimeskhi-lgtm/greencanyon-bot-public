import re
import os
import json
import xml.etree.ElementTree as ET
import math

svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"

# Re-use the parser but only keep 2-point segments
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

print(f"Total paths to process: {len(paths)}")

segments = []
for idx, p in enumerate(paths):
    d = p.attrib.get('d', '')
    if not d:
        continue
    transform = p.attrib.get('transform', '')
    try:
        pts = parse_path_d(d)
        if len(pts) == 2:
            # Apply transform
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

print(f"Extracted {len(segments)} segments.")

# Join segments into polygons (loops)
# We can find loops by matching endpoints. We'll use a threshold of 0.2 pixels.
TOL = 0.2

def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Build adjacency list
# Each point will map to its connected points
adj = {}
def add_edge(p1, p2):
    # Find matching vertices in adj
    v1 = None
    for k in adj:
        if dist(k, p1) < TOL:
            v1 = k
            break
    if v1 is None:
        v1 = p1
        adj[v1] = []
        
    v2 = None
    for k in adj:
        if dist(k, p2) < TOL:
            v2 = k
            break
    if v2 is None:
        v2 = p2
        adj[v2] = []
        
    # Prevent duplicate edges
    if v2 not in adj[v1]:
        adj[v1].append(v2)
    if v1 not in adj[v2]:
        adj[v2].append(v1)

for s in segments:
    add_edge(s[0], s[1])

print(f"Graph constructed: {len(adj)} unique vertices.")

# Let's find cycles (loops) in the graph
visited = set()
polygons = []

for start_node in list(adj.keys()):
    if start_node in visited:
        continue
    # We want to find closed loops. If degree of node is not 2, it's not a simple loop vertex
    if len(adj[start_node]) != 2:
        continue
        
    # Traverse the loop
    loop = [start_node]
    curr = start_node
    prev = None
    loop_closed = False
    
    while True:
        neighbors = [n for n in adj[curr] if n != prev]
        if not neighbors:
            break
        # Pick the first neighbor
        nxt = neighbors[0]
        if nxt == start_node:
            loop_closed = True
            break
        if nxt in visited or nxt in loop:
            # self-intersection or already part of another visited area
            break
        loop.append(nxt)
        prev = curr
        curr = nxt
        
    if loop_closed and len(loop) >= 3:
        for node in loop:
            visited.add(node)
        polygons.append(loop)

print(f"Reconstructed {len(polygons)} closed polygons from line segments.")

# Print some polygons details
if polygons:
    print(f"Sizes of first 10 polygons: {[len(p) for p in polygons[:10]]}")
    # let's check if their centroids range matches plots
    cxs = []
    cys = []
    for poly in polygons:
        cx = sum(p[0] for p in poly) / len(poly)
        cy = sum(p[1] for p in poly) / len(poly)
        cxs.append(cx)
        cys.append(cy)
    print(f"Reconstructed centroids X range: {min(cxs):.2f} to {max(cxs):.2f}")
    print(f"Reconstructed centroids Y range: {min(cys):.2f} to {max(cys):.2f}")
