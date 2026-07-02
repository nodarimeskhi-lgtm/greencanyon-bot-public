import os

search_words = ["იმერი", "მარგველი", "განმარტება", "ვაულინი"]
folders = [r"c:\Users\Nodar\2026 antigraviti", r"c:\Users\Nodar\Batumi Hills"]

for folder in folders:
    print(f"\nSearching in {folder}...")
    for root, dirs, files in os.walk(folder):
        # Skip some standard directories to speed up
        if any(p in root for p in [".git", "node_modules", ".cursor", ".agent", "scratch"]):
            continue
        for file in files:
            if file.endswith((".txt", ".md", ".docx", ".xlsx")):
                file_path = os.path.join(root, file)
                try:
                    # For excel/docx we just check file name, for text files we check content
                    if file.endswith((".txt", ".md")):
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            found = [w for w in search_words if w in content or w in file]
                            if found:
                                print(f"Found in content of {file_path}: {found}")
                    else:
                        found = [w for w in search_words if w in file]
                        if found:
                            print(f"Found in filename {file_path}: {found}")
                except Exception as e:
                    pass
