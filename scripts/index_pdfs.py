import os
import pdfplumber
from app.utils.pinecone_indexer import index_document


PDF_DIR = "./data/pdfs"


for fname in os.listdir(PDF_DIR):
    if not fname.lower().endswith('.pdf'):
        continue
    path = os.path.join(PDF_DIR, fname)
    text = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            txt = page.extract_text() or ""
            text.append(txt)
    full_text = "\n\n".join(text)
    doc_id = os.path.splitext(fname)[0]
    index_document(doc_id=doc_id, title=doc_id, text=full_text, metadata={"source_file": fname})