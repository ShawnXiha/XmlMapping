from typing import Dict, List, Tuple
from lxml import etree


def get_aligned_nodes(xsd_file1: str, xsd_file2: str) -> Dict[Tuple[str, str], Tuple[str, str]]:
    """
    Given two XSD files, extracts the local names of all elements and attributes and
    the text values of all xsl:document sub-elements. Computes the similarity score
    between each pair of nodes based on their local names and xsl:document sub-element
    text values. Returns a dictionary of aligned nodes, where each key-value pair
    corresponds to a pair of aligned nodes from the two XSD files.
    """
    xsd_ns = {'xs': 'http://www.w3.org/2001/XMLSchema', 'xsl': 'http://www.w3.org/1999/XSL/Transform'}

    def get_xsd_nodes(xsd_file: str) -> List[Tuple[str, str]]:
        xsd_tree = etree.parse(xsd_file)
        xsd_root = xsd_tree.getroot()

        nodes = []

        for elem in xsd_root.iter():
            if 'name' in elem.attrib:
                node_name = elem.attrib['name']
                nodes.append((node_name.lower(), ''))
            if 'type' in elem.attrib:
                node_type = elem.attrib['type']
                if ':' in node_type:
                    node_type = node_type.split(':')[-1]
                nodes.append((node_type.lower(), ''))
            if elem.tag == '{http://www.w3.org/1999/XSL/Transform}document':
                for child in elem.iter():
                    if child.text is not None:
                        nodes.append((child.text.lower(), child.text))

        return nodes

    def compute_similarity_score(node1: Tuple[str, str], node2: Tuple[str, str]) -> float:
        name_similarity = 0.5 if node1[0] == node2[0] else 0
        text_similarity = 0.5 if node1[1] == node2[1] else 0
        return name_similarity + text_similarity

    nodes1 = get_xsd_nodes(xsd_file1)
    nodes2 = get_xsd_nodes(xsd_file2)

    similarity_scores = {}
    for node1 in nodes1:
        for node2 in nodes2:
            similarity_scores[(node1, node2)] = compute_similarity_score(node1, node2)

    aligned_nodes = {}
    for node1 in nodes1:
        max_score = 0
        max_node = None
        for node2 in nodes2:
            score = similarity_scores[(node1, node2)]
            if score > max_score:
                max_score = score
                max_node = node2
        if max_node is not None:
            aligned_nodes[node1] = max_node

    return aligned_nodes


if __name__ == '__main__':
    aligned_nodes = get_aligned_nodes('schema1.xsd', 'schema2.xsd')
    print(aligned_nodes)
