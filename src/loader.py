import fitz  # PyMuPDF

def load_pdf(pdf_path: str) -> list[dict]:
    """
    Extract text from each page of a PDF.
    Returns a list of dicts with page number and text.
    """
    doc = fitz.open(pdf_path)
    documents = []    

    for page_num, page in enumerate(doc, start=1):  #as page_num start from 1 and python enumerate starts from 0
        text = page.get_text()

        if not text.strip():   #skip empty pages 
            continue

        #clean up texts 
        text = text.replace("\n", " ") 
        text = " ".join(text.split())
        documents.append({
            "page": page_num,
            "text": text
            })
        
    doc.close()
    return documents













