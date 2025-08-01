# src/data_processing/normalizer.py

import re

class TextNormalizer:
    def normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'([.?!])\s+', r'\1\n', text)  # sentence split
        return text.strip()
