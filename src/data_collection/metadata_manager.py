# src/data_collection/metadata_manager.py
import csv, os

class MetadataManager:
    def __init__(self, csv_path="data/sources.csv"):
        self.csv_path = csv_path
        if not os.path.exists(csv_path):
            with open(csv_path, "w", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["file", "title", "source_url", "section"])
                writer.writeheader()

    def log(self, file: str, title: str, source_url: str, section: str):
        with open(self.csv_path, "a", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["file", "title", "source_url", "section"])
            writer.writerow({
                "file": file,
                "title": title,
                "source_url": source_url,
                "section": section
            })
