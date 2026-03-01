import os
from grobid_client.grobid_client import GrobidClient

# Connect to running GROBID server
client = GrobidClient(config_path=None)


def process_pdf_folder(pdf_folder=".", output_folder="grobid_output"):

    # Create output folder if not exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, file)
            print(f"Processing {file}...")

            client.process(
                "processFullTextDocument",
                pdf_path,
                output=output_folder,
                consolidate_header=True
            )

    print("All PDFs processed successfully.")