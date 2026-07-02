import os

base_dir = r"c:\Users\Nodar\2026 antigraviti"
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if "interactive" in file.lower() or "map" in file.lower():
            print(os.path.join(root, file))
