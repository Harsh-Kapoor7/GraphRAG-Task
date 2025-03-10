import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    raw_text = " ".join([page.extract_text() for page in reader.pages])
    return raw_text

def extract_images_from_pdf(pdf_path):
    folder = 'extracted_images'
    os.makedirs(folder, exist_ok=True)
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, img in enumerate(images):
        image_path = os.path.join(folder, f"page_{i+1}.png")
        img.save(image_path, 'png')
        image_paths.append(image_path)
    return image_paths

def extract_text_from_images(image_paths):
    return "\n".join(pytesseract.image_to_string(img) for img in image_paths).strip()

def extract_text_and_images(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    image_paths = extract_images_from_pdf(pdf_path)
    image_text = extract_text_from_images(image_paths) if image_paths else ""
    return text + "\n" + image_text, image_paths

def split_text_into_chunks(full_text, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(full_text)