import xml.etree.ElementTree as ET
import re

svg_path = r"c:\Users\Nodar\2026 antigraviti\05-Projects\Tsalka\6-Sales\6-4-Marketing\2025PRV05TGGM-2026-FEB-5.svg"

tree = ET.parse(svg_path)
root = tree.getroot()

# Traverse the SVG and count paths in each group, printing the hierarchy and transforms
def inspect_group(element, depth=0):
    tag = element.tag.split('}')[-1]
    attrib_id = element.attrib.get('id', '')
    transform = element.attrib.get('transform', '')
    
    # count direct path children
    paths = [c for c in element if c.tag.split('}')[-1] == 'path']
    child_groups = [c for c in element if c.tag.split('}')[-1] == 'g']
    
    indent = "  " * depth
    if tag == 'g' or len(paths) > 0:
        print(f"{indent}Group ID: '{attrib_id}', transform: '{transform}', direct paths: {len(paths)}, child groups: {len(child_groups)}")
        
    for child in child_groups:
        inspect_group(child, depth + 1)

inspect_group(root)
