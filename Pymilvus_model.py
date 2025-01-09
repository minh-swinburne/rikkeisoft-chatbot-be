import os
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
docs = []

for file_path in file_paths:
    try:
        text = extract_text_from_file(file_path)
        docs.append(text)
    except ValueError as e:
        print(f"Error processing {file_path}: {e}")

# Encode the documents
docs_embeddings = sentence_transformer_ef.encode_documents(docs)

# Print embeddings
print("Embeddings:", docs_embeddings)
# Print dimension and shape of embeddings
print("Dim:", sentence_transformer_ef.dim, docs_embeddings[0].shape)
