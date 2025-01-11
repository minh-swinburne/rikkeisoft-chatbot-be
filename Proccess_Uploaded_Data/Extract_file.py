import os
import fitz  # PyMuPDF for PDF
from PIL import Image
import pytesseract
from docx import Document  # python-docx for DOCX
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Admin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def extract_images_from_pdf(pdf_path):
    """Extract images from a PDF."""
    pdf_document = fitz.open(pdf_path)
    images = []
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append((page_num + 1, img_index + 1, image))
    return images

def extract_text_from_pdf(pdf_path):
    """Extract text and perform OCR on images within a PDF document."""
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page in pdf_document:
        text += page.get_text()

    # Perform OCR on images in the PDF
    images = extract_images_from_pdf(pdf_path)
    for page_num, img_index, image in images:
        ocr_text = pytesseract.image_to_string(image)
        text += f"\nOCR - Page {page_num}, Image {img_index}:\n{ocr_text}\n"
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

# You can export this module if needed, but this file mainly handles extraction.
