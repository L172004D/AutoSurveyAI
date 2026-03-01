from grobid_client.grobid_client import GrobidClient

def process_all_pdfs():
    client = GrobidClient(config_path=None)

    client.process(
        "processFulltextDocument",
        input_path=".",                 # Current folder
        output="grobid_output",         # Output folder
        consolidate_header=True,
        consolidate_citations=True,
        tei_coordinates=True
    )

if __name__ == "__main__":
    print("Processing all PDFs in current folder...")
    process_all_pdfs()
    print("Done.")