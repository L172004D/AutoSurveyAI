import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from parse import parse_tei_xml

XML_FOLDER = "grobid_output"
INDEX_PATH = "research_index.faiss"

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_all_sections():
    all_sections = []

    for file in os.listdir(XML_FOLDER):
        if file.endswith(".xml"):
            xml_path = os.path.join(XML_FOLDER, file)
            data = parse_tei_xml(xml_path)

            if isinstance(data, dict) and "sections" in data:
                for sec in data["sections"]:
                    all_sections.append(sec)

    return all_sections


def build_index():
    print("Loading all XML files...")
    sections = load_all_sections()
    print(f"Total sections collected: {len(sections)}")

    print("Generating embeddings...")
    embeddings = model.encode(sections)

    print("Creating FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    print("Saving index...")
    faiss.write_index(index, INDEX_PATH)
    print("Index saved successfully.")


if __name__ == "__main__":
    build_index()