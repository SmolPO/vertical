import xml.etree.ElementTree as ET


def create_file(data):
    root = ET.Element("xml")
    item_boss = ET.SubElement(root, "boss")
    item_boss.text = "boss"
    item_name = ET.SubElement(root, "name")
    item_name.text = "name"
    item_list = ET.SubElement(root, "list")
    for item in ["ads", "asdd", "wer"]:
        el = ET.SubElement(item_list, "worker")
        el.text = item
    tree = ET.ElementTree(root)
    tree.write("xml_test.xml")
# открыть или создать
try:
    tree = ET.parse("xml_test.xml")
    glob_root = tree.getroot()
    root = ET.SubElement(glob_root, "pattern")
    item_boss = ET.SubElement(root, "boss")
    item_boss.text = "boss"
    item_name = ET.SubElement(root, "name")
    item_name.text = "name"
    item_list = ET.SubElement(root, "list")
    for item in ["ads", "asdd", "wer"]:
        el = ET.SubElement(item_list, "worker")
        el.text = item
    tree.write("xml_test.xml")
except:
    create_file(["jgh1", "jbj2", "hj3"])
    pass



# добавить элемент
# найти элемент
# удалить элемент
