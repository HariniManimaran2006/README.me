"""
Text extraction module for PDF, DOCX, and TXT files.
"""
import io
from typing import Optional


def extract_text_from_file(uploaded_file) -> str:
    """
    Extract text from uploaded file (PDF, DOCX, or TXT).
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        Extracted text as string
    """
    name = uploaded_file.name.lower()
    data = uploaded_file.getvalue()
    
    if name.endswith(".pdf"):
        return _extract_pdf(data)
    elif name.endswith(".docx"):
        return _extract_docx(data)
    elif name.endswith(".txt"):
        return _extract_txt(data)
    else:
        return "[Unsupported file type]"


def _extract_pdf(data: bytes) -> str:
    """Extract text from PDF data."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(data))
        texts = []
        for page in reader.pages:
            text = page.extract_text() or ""
            if text.strip():
                texts.append(text)
        return "\n\n".join(texts) if texts else "[No text extracted from PDF]"
    except Exception as e:
        return f"[PDF extraction error: {str(e)}]"


def _extract_docx(data: bytes) -> str:
    """Extract text from DOCX data."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(data))
        texts = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(texts) if texts else "[No text extracted from DOCX]"
    except Exception as e:
        return f"[DOCX extraction error: {str(e)}]"


def _extract_txt(data: bytes) -> str:
    """Extract text from TXT file."""
    try:
        return data.decode("utf-8", errors="replace")
    except Exception as e:
        return f"[TXT decode error: {str(e)}]"
