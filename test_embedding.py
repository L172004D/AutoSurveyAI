from parse import parse_tei_xml
from embedding_module import generate_embeddings, create_faiss_index, search_similar

# Load structured data
data = parse_tei_xml("grobid_output/sample.tei.xml")

sections = data["sections"]

# Generate embeddings
embeddings = generate_embeddings(sections)

# Create FAISS index
index = create_faiss_index(embeddings)

# Search
query = "deep learning method"
results = search_similar(index, query, sections)

print("Top Similar Sections:")
for r in results:
    print("-", r[:200])