from parse import parse_tei_xml
from embedding_module import generate_embeddings
import numpy as np


def compute_similarity(paper1_xml, paper2_xml):
    data1 = parse_tei_xml(paper1_xml)
    data2 = parse_tei_xml(paper2_xml)

    text1 = " ".join(data1["sections"])
    text2 = " ".join(data2["sections"])

    embeddings = generate_embeddings([text1, text2])

    vec1 = embeddings[0]
    vec2 = embeddings[1]

    similarity = np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )

    return similarity


if __name__ == "__main__":
    paper1 = "grobid_output/sample.tei.xml"
    paper2 = "grobid_output/sample.tei.xml"   # change if you have second paper

    score = compute_similarity(paper1, paper2)

    print("\nPaper Similarity Score:", round(float(score), 4))