# src/data_processing/cleaner.py

import re

class TextCleaner:
    def __init__(self):
        self.previous_blocks = set()

    def clean_text(self, text: str) -> str:
        # Remove non-ASCII or strange characters
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)

        # Remove lines that are just page numbers, headers, etc.
        lines = text.splitlines()
        clean_lines = []
        for line in lines:
            line = line.strip()
            if len(line) < 3 or line.lower() in self.previous_blocks:
                continue
            if re.match(r'^page\s*\d+$', line.lower()):
                continue
            if line:
                clean_lines.append(line)
                self.previous_blocks.add(line.lower())
        return "\n".join(clean_lines)
