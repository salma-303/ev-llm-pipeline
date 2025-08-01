# src/data_collection/pdf_extractor.py

import fitz  # PyMuPDF
import os
import logging

class PDFExtractor:
    def __init__(self, base_dir="data/raw"):
        self.base_dir = base_dir
        self.logger = logging.getLogger(__name__)
    
    def extract_with_layout(self, pdf_path: str) -> str:
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                blocks = page.get_text("blocks")  # returns list of tuples
                page_text = "\n".join([b[4] for b in blocks if len(b) > 4])
                text += page_text + "\n\n"
            return text
        except Exception as e:
            self.logger.error(f"PDF extraction failed: {e}")
            return ""
