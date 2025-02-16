import wikipediaapi
import time
import xml.etree.ElementTree as ET
import re

def explore_node(xml_nodes, edges, node, node_set):
    try:
        page = wiki_wiki.page(node)
        txt = page.text

        base_node = ET.SubElement(xml_nodes, "node", name=node)

        ET.SubElement(base_node, "text").text = txt
      
    except:
        print(f'Error on {node}. Waiting...')
        time.sleep(2)

def create_tree(tree, nodes_to_explore):

    nodes = ET.SubElement(tree, "nodes")

    total_nodes = len(nodes_to_explore)
    
    for i, node in enumerate(nodes_to_explore):
        explore_node(nodes, edges, node, nodes_to_explore)
        time.sleep(0.9)
        
        percent_done = ((i + 1) / total_nodes) * 100
    
        if percent_done % 5 == 0:
            print(f"{int(percent_done)}% done")

    return



if __name__ == "__main__":
    with open("../../EMAIL",'r') as f:
        email = f.readlines()[0]

    wiki_wiki = wikipediaapi.Wikipedia(f'WikiPhilosophy Graph ({email})', 'en')
    mems = []
    def gather_cat_mems(categorymembers, level=0, max_level=1):
        for c in categorymembers.values():
            if c.ns ==wikipediaapi.Namespace.MAIN:
                mems.append(c.title)
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                time.sleep(1)
                gather_cat_mems(c.categorymembers, level=level + 1, max_level=max_level)

    cats = ["Category:Philosophers_by_field","Category:Philosophical_schools_and_traditions","Category:Philosophical_concepts", "Category:Branches_of_philosophy"]

    for c in cats:
        cat_mems = wiki_wiki.page(c).categorymembers
        gather_cat_mems(cat_mems, max_level=1)

    print("Step 1: Done")

    tree_root = ET.Element("dataset")
    create_tree(tree_root, mems)
    tree = ET.ElementTree(tree_root)
    ET.indent(tree, "\t", level=0)
    tree.write("FILEHERE")
