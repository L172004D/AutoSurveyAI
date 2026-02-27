from grobid_module import extract_structured

xml_file = extract_structured("sample.pdf")
print("Generated XML file at:", xml_file)