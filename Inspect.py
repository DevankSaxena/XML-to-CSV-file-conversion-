import xml.etree.ElementTree as ET

def inspect_xml_structure(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    def recurse_tree(element, level=0):
        indent = "  " * level
        print(f"{indent}Tag: {element.tag}, Attributes: {element.attrib}")
        for child in element:
            recurse_tree(child, level + 1)

    print(f"Root tag: {root.tag}")
    recurse_tree(root)

# Usage
xml_file = "/mnt/data/A20200314.1200+0200-1230+0200_MBTS_06330_VO_BBU0_IERAPETRA_NORTH.xml"
inspect_xml_structure(xml_file)
