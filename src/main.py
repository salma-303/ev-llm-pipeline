import yaml
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_collection.scraper import EVWebScraper
from src.data_collection.pdf_extractor import PDFExtractor
from src.data_collection.metadata_manager import MetadataManager

def load_config(path="config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def run_data_collection():
    config = load_config()
    sources = config["data_collection"]["sources"]
    raw_dir = config["data_collection"]["raw_dir"]
    meta_file = config["data_collection"]["metadata_file"]

    scraper = EVWebScraper(base_dir=raw_dir)
    pdf_extractor = PDFExtractor(base_dir=raw_dir)
    meta = MetadataManager(csv_path=meta_file)

    for entry in sources:
        title = entry["title"]
        section = entry["section"]
        filename = f"{title.lower().replace(' ', '_').replace('-', '').replace('–', '').replace(':', '')}.txt"

        if entry["type"] == "url":
            url = entry["url"]
            saved_path = scraper.fetch_and_save(url, filename)
            if saved_path:
                meta.log(file=filename, title=title, source_url=url, section=section)

        elif entry["type"] == "pdf":
            pdf_path = entry["file_path"]
            text = pdf_extractor.extract_with_layout(pdf_path)
            saved_path = os.path.join(raw_dir, filename)
            with open(saved_path, "w", encoding="utf-8") as f:
                f.write(text)
            meta.log(file=filename, title=title, source_url=pdf_path, section=section)

if __name__ == "__main__":
    run_data_collection()
