# src/data_processing/processor.py

import os
import json
import logging
from src.data_processing.cleaner import TextCleaner
from src.data_processing.normalizer import TextNormalizer

class DataProcessor:
    def __init__(self, input_dir, output_dir):
        self.cleaner = TextCleaner()
        self.normalizer = TextNormalizer()
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def process_all(self):
        self.logger.info("Starting data processing...")
        for filename in os.listdir(self.input_dir):
            if not filename.endswith(".txt"):
                continue

            try:
                input_path = os.path.join(self.input_dir, filename)
                with open(input_path, "r", encoding="utf-8") as f:
                    raw = f.read()

                cleaned = self.cleaner.clean_text(raw)
                normalized = self.normalizer.normalize(cleaned)
                structured = self.split_to_blocks(normalized)

                output_path = os.path.join(self.output_dir, filename.replace(".txt", ".jsonl"))
                with open(output_path, "w", encoding="utf-8") as out_f:
                    for block in structured:
                        json.dump(block, out_f)
                        out_f.write("\n")

                self.logger.info(f"Processed: {filename} → {output_path}")
            except Exception as e:
                self.logger.error(f"Failed to process {filename}: {e}")

    def split_to_blocks(self, text: str):
        try:
            sentences = text.split("\n")
            blocks = []
            block = []

            for s in sentences:
                if len(s.strip().split()) > 5:
                    block.append(s.strip())

                if len(block) >= 3:
                    blocks.append({"text": " ".join(block)})
                    block = []

            if block:
                blocks.append({"text": " ".join(block)})

            return blocks
        except Exception as e:
            self.logger.error(f"Error during block segmentation: {e}")
            return []
