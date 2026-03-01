\# AI Research Paper Semantic Search Engine



This project allows:

\- Uploading research papers

\- Extracting structure using GROBID

\- Generating embeddings

\- Creating FAISS index

\- Performing semantic search via Web UI



---



\## Installation



1\. Clone the repository:



git clone https://github.com/YOUR\_USERNAME/AUTO-SURVEY.git

cd AUTO-SURVEY



2\. Install dependencies:



pip install -r requirements.txt



3\. Start GROBID server (Docker required):



docker run --rm -p 8070:8070 grobid/grobid:0.8.0



4\. Run the application:



python -m streamlit run app.py



---



\## Open in browser:

http://localhost:8501

