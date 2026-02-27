from lxml import etree
import json

def parse_grobid_xml(xml_path):
    tree = etree.parse(xml_path)
    root = tree.getroot()

    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

    # Extract title
    title = root.find('.//tei:titleStmt/tei:title', ns)
    title_text = title.text if title is not None else "N/A"

    # Extract authors
    authors = []
    for author in root.findall('.//tei:author', ns):
        forename = author.find('.//tei:forename', ns)
        surname = author.find('.//tei:surname', ns)
        name = ""
        if forename is not None:
            name += forename.text + " "
        if surname is not None:
            name += surname.text
        if name.strip():
            authors.append(name.strip())

    # Extract abstract
    abstract = root.find('.//tei:abstract//tei:p', ns)
    abstract_text = abstract.text if abstract is not None else "N/A"

    # Extract sections
    sections = []
    for div in root.findall('.//tei:body//tei:div', ns):
        section_text = " ".join(div.xpath('.//tei:p/text()', namespaces=ns))
        if section_text.strip():
            sections.append(section_text.strip())

    # Extract references
    references = []
    for ref in root.findall('.//tei:listBibl//tei:biblStruct', ns):
        ref_text = " ".join(ref.xpath('.//tei:title/text()', namespaces=ns))
        if ref_text.strip():
            references.append(ref_text.strip())

    data = {
        "title": title_text,
        "authors": authors,
        "abstract": abstract_text,
        "sections": sections,
        "references": references
    }

    return data


if __name__ == "__main__":
    xml_file = "grobid_output/sample.tei.xml"
    result = parse_grobid_xml(xml_file)

    print(json.dumps(result, indent=4))