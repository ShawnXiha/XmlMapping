
# XML Mapping Tool From XSD TO XSLT

The XML Mapping Tool is a Python package that helps you create mappings between two XML files with different XSD schemas.

## Installation
To install the XML Mapping Tool, clone the repository and install the required dependencies with pip:

Install lxml
```bash
    pip install -r lxml 
```


Usage
To use the XML Mapping Tool, run the mapping_tool.py script and provide the paths to the two XSD files:

step1:

generate xslt from xsd schema files
```python
from mapping2xslt import generate_xslt_files
generate_xslt_files('schema1.xsd', 'schema2.xsd', 'schema1_to_schema2.xslt', 'schema2_to_schema1.xslt')
```

step2:

xml to xml with the xslt generated


```python
from xml2xmlwithxslt import translate_xml
xml_result = translate_xml(xml_string, xslt_file)
```
