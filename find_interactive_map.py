import os

base_dir = r"c:\Users\Nodar\2026 antigraviti"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file == "interactive_map.html":
            print(os.path.join(root, file))
