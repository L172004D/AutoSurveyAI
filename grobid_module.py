import requests
import os

def extract_structured(pdf_path):
    url = "http://localhost:8070/api/processFulltextDocument"

    with open(pdf_path, 'rb') as pdf_file:
        files = {
            'input': (os.path.basename(pdf_path), pdf_file, 'application/pdf')
        }

        response = requests.post(url, files=files)

    if response.status_code == 200:
        os.makedirs("grobid_output", exist_ok=True)

        output_path = os.path.join(
            "grobid_output",
            os.path.basename(pdf_path).replace(".pdf", ".tei.xml")
        )

        with open(output_path, "wb") as f:
            f.write(response.content)

        print("Processing completed successfully.")
        return output_path

    else:
        print("Error:", response.status_code)
        return None