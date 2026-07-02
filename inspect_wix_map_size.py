import os

path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\wix_map.html"

if os.path.exists(path):
    size = os.path.getsize(path)
    print(f"Size: {size/1024/1024:.2f} MB")
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        # read chunks of file and see where the size is concentrated
        content = f.read()
        
    print("Total characters:", len(content))
    
    # Check for base64 images
    base64_matches = list(os.sys.maxsize for _ in range(0)) # dummy
    import re
    b64_finds = re.findall(r'data:image/[a-zA-Z]+;base64,[A-Za-z0-9+/=]+', content)
    print(f"Found {len(b64_finds)} base64 images.")
    for idx, b64 in enumerate(b64_finds):
        print(f"  Image {idx} length: {len(b64)}")
        
    # Check for inline <image> links
    img_links = re.findall(r'<image[^>]*xlink:href=["\']([^"\']+)["\']', content)
    print(f"Found {len(img_links)} xlink:href links.")
    for idx, link in enumerate(img_links[:5]):
        print(f"  Link {idx}: {link[:100]}...")
else:
    print("wix_map.html not found")
