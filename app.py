import streamlit as st
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from parse import parse_tei_xml

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="AI Research Paper Search Engine",
    layout="wide",
)

MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = "research_index.faiss"
XML_FOLDER = "grobid_output"

model = SentenceTransformer(MODEL_NAME)

# -------------------------
# TITLE
# -------------------------
st.title("📚 AI Research Paper Semantic Search Engine")
st.markdown("Upload → Extract → Index → Search Across Multiple Papers")

st.divider()

# -------------------------
# FILE UPLOAD
# -------------------------
uploaded_files = st.file_uploader(
    "Upload PDF Papers",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())
    st.success("Files uploaded successfully!")

# -------------------------
# PROCESS BUTTON
# -------------------------
if st.button("🔄 Process & Index Papers"):
    st.info("Make sure GROBID server is running on port 8070...")
    os.system("python batch_grobid.py")
    os.system("python multi_paper_pipeline.py")
    st.success("Processing & Indexing Completed!")

st.divider()

# -------------------------
# LOAD INDEX + SECTIONS
# -------------------------
def load_all_sections():
    all_sections = []
    section_sources = []

    for file in os.listdir(XML_FOLDER):
        if file.endswith(".xml"):
            xml_path = os.path.join(XML_FOLDER, file)
            data = parse_tei_xml(xml_path)

            if isinstance(data, dict) and "sections" in data:
                for sec in data["sections"]:
                    all_sections.append(sec)
                    section_sources.append(file.replace(".tei.xml", ""))

    return all_sections, section_sources


# -------------------------
# SEARCH SECTION
# -------------------------
st.header("🔎 Semantic Search")

query = st.text_input("Enter your research query")

if query:

    if not os.path.exists(INDEX_PATH):
        st.error("Index not found. Please process papers first.")
    else:
        st.info("Searching...")

        # Load index
        index = faiss.read_index(INDEX_PATH)

        # Load sections
        sections, sources = load_all_sections()

        # Embed query
        query_embedding = model.encode([query])
        D, I = index.search(np.array(query_embedding), k=5)

        st.subheader("Top Matching Results")

        for rank, idx in enumerate(I[0]):
            if idx < len(sections):

                score = 1 - D[0][rank]  # similarity score
                paper_name = sources[idx]
                section_text = sections[idx]

                st.markdown("---")
                st.markdown(f"### 📄 Paper: {paper_name}")
                st.markdown(f"**Similarity Score:** {score:.4f}")
                st.write(section_text[:1000])

st.divider()

st.markdown("Built with ❤️ using GROBID + FAISS + SentenceTransformers")