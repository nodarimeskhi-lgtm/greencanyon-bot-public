import os
import json

base_dir = r"c:\Users\Nodar\2026 antigraviti"

for root, dirs, files in os.walk(base_dir):
    if 'node_modules' in root or '.git' in root or '.netlify' in root:
        continue
    for file in files:
        if file.endswith('.json'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    sample = data[0]
                    if isinstance(sample, dict):
                        print(f"File: {file} (list of dicts, length {len(data)})")
                        print(f"  Sample keys: {list(sample.keys())}")
                        # Check for coordinates, points, polygons, etc.
                        for key in ['points', 'coordinates', 'geometry', 'polygon', 'vertices']:
                            if key in sample:
                                print(f"  --> FOUND GEOMETRY KEY: '{key}' in {file}")
                elif isinstance(data, dict) and len(data) > 0:
                    print(f"File: {file} (dict, length {len(data)})")
                    print(f"  Sample keys: {list(data.keys())[:10]}")
                    first_key = list(data.keys())[0]
                    if isinstance(data[first_key], dict):
                        print(f"    Sub-keys: {list(data[first_key].keys())}")
            except Exception as e:
                print(f"Error reading {file}: {e}")
