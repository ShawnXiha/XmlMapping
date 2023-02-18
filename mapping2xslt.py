from lxml import etree

from xsd2mapping import get_aligned_nodes


def generate_xslt_files(xsd_file1: str, xsd_file2: str, xslt_file1: str, xslt_file2: str):
    """
    Given two XSD files and two XSLT file paths, generates XSLT files that can translate
    XML documents from one schema to the other and vice versa, and saves the XSLT files
    to disk.
    """
    aligned_nodes = get_aligned_nodes(xsd_file1, xsd_file2)

    # Generate XSLT file 1 (from schema 1 to schema 2)
    root = etree.Element('{http://www.w3.org/1999/XSL/Transform}stylesheet', version='1.0',
                         xmlns='http://www.w3.org/1999/XSL/Transform')

    # Create a template that matches the root element of schema 1
    template1 = etree.SubElement(root, '{http://www.w3.org/1999/XSL/Transform}template', match='/*')
    apply_template1 = etree.SubElement(template1, '{http://www.w3.org/1999/XSL/Transform}apply-templates')

    # Create a template for each aligned node, and add a copy-of instruction to copy the node
    for node1, node2 in aligned_nodes.items():
        template1 = etree.SubElement(root, '{http://www.w3.org/1999/XSL/Transform}template', match=node1[0])
        copy_of = etree.SubElement(template1, '{http://www.w3.org/1999/XSL/Transform}copy-of', select='.')

    # Generate XSLT file 2 (from schema 2 to schema 1)
    root = etree.Element('{http://www.w3.org/1999/XSL/Transform}stylesheet', version='1.0',
                         xmlns='http://www.w3.org/1999/XSL/Transform')

    # Create a template that matches the root element of schema 2
    template2 = etree.SubElement(root, '{http://www.w3.org/1999/XSL/Transform}template', match='/*')
    apply_template2 = etree.SubElement(template2, '{http://www.w3.org/1999/XSL/Transform}apply-templates')

    # Create a template for each aligned node, and add a copy-of instruction to copy the node
    for node2, node1 in aligned_nodes.items():
        template2 = etree.SubElement(root, '{http://www.w3.org/1999/XSL/Transform}template', match=node2[0])
        copy_of = etree.SubElement(template2, '{http://www.w3.org/1999/XSL/Transform}copy-of', select='.')

    # Save the XSLT files to disk
    xslt_tree1 = etree.ElementTree(root)
    xslt_tree1.write(xslt_file1, encoding='UTF-8', pretty_print=True)

    xslt_tree2 = etree.ElementTree(root)
    xslt_tree2.write(xslt_file2, encoding='UTF-8', pretty_print=True)


if __name__ == '__main__':
    generate_xslt_files('schema1.xsd', 'schema2.xsd', 'schema1_to_schema2.xslt', 'schema2_to_schema1.xslt')
