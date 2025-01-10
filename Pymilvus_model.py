import os
import json
from pymilvus import model
import pymupdf  # PyMuPDF for PDF
from docx import Document  # python-docx for DOCX

# Initialize SentenceTransformerEmbeddingFunction
sentence_transformer_ef = model.dense.SentenceTransformerEmbeddingFunction(
    model_name='all-MiniLM-L6-v2',
    device='cpu'
)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF document."""
    doc = pymupdf.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX document."""
    doc = Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_file(file_path):
    """Extract text from a file (PDF or DOCX)."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

# Example usage
file_paths = ["example.pdf"]
output_data = []

# Define output JSON path
output_json_path = "output_data.json"

# Load existing data if the file exists
if os.path.exists(output_json_path):
    with open(output_json_path, "r", encoding="utf-8") as json_file:
        try:
            output_data = json.load(json_file)
        except json.JSONDecodeError:
            print("Warning: Could not decode existing JSON file. Starting fresh.")

existing_files = {item["file_name"] for item in output_data}  # Track processed files

for file_path in file_paths:
    file_name = os.path.basename(file_path)
    if file_name in existing_files:
        print(f"File {file_name} has already been processed. Skipping.")
        continue
    try:
        text = extract_text_from_file(file_path)
        embedding = sentence_transformer_ef.encode_documents([text])[0]  # Encode the text and get the first embedding
        output_data.append({
            "file_name": file_name,
            "embedding": embedding.tolist()  # Convert NumPy array to list for JSON serialization
        })
    except ValueError as e:
        print(f"Error processing {file_path}: {e}")

# Save the updated data to the JSON file
with open(output_json_path, "w", encoding="utf-8") as json_file:
    json.dump(output_data, json_file, indent=4, ensure_ascii=False)

print(f"Data saved to {output_json_path}")
