import logging
import yaml
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_collection.scraper import EVWebScraper
from src.data_collection.pdf_extractor import PDFExtractor
from src.data_collection.metadata_manager import MetadataManager
from src.data_processing.processor import DataProcessor


def setup_logger():
    logger = logging.getLogger("EVPipeline")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def load_config(path="config/config.yaml"):
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load config from {path}: {e}")
        raise


def run_data_collection(config, logger):
    try:
        sources = config["data_collection"]["sources"]
        raw_dir = config["data_collection"]["raw_dir"]
        meta_file = config["data_collection"]["metadata_file"]

        scraper = EVWebScraper(base_dir=raw_dir)
        pdf_extractor = PDFExtractor(base_dir=raw_dir)
        meta = MetadataManager(csv_path=meta_file)

        for entry in sources:
            try:
                title = entry["title"]
                section = entry["section"]
                filename = f"{title.lower().replace(' ', '_').replace('-', '').replace('–', '').replace(':', '')}.txt"
                logger.info(f"Processing source: {title}")

                if entry["type"] == "url":
                    url = entry["url"]
                    saved_path = scraper.fetch_and_save(url, filename)
                    if saved_path:
                        meta.log(file=filename, title=title, source_url=url, section=section)
                        logger.info(f"Saved and logged URL content for: {title}")

                elif entry["type"] == "pdf":
                    pdf_path = entry["file_path"]
                    text = pdf_extractor.extract_with_layout(pdf_path)
                    saved_path = os.path.join(raw_dir, filename)
                    with open(saved_path, "w", encoding="utf-8") as f:
                        f.write(text)
                    meta.log(file=filename, title=title, source_url=pdf_path, section=section)
                    logger.info(f"Extracted and logged PDF content for: {title}")

                else:
                    logger.warning(f"Unknown source type for {title}: {entry.get('type')}")

            except Exception as e:
                logger.error(f"Failed to process source '{entry.get('title', 'unknown')}': {e}")

        logger.info(f"Data collection complete. Files saved in '{raw_dir}'")

    except Exception as e:
        logger.critical(f"Data collection failed: {e}")
        raise


def run_data_processing(logger):
    try:
        processor = DataProcessor(
            input_dir="data/raw",
            output_dir="data/processed"
        )
        processor.process_all()
        logger.info("Data processing complete.")
    except Exception as e:
        logger.critical(f"Data processing failed: {e}")
        raise


if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Starting EV Data Pipeline...")

    try:
        config = load_config()
        run_data_collection(config, logger)
        run_data_processing(logger)
        logger.info("Pipeline execution finished successfully.")
    except Exception:
        logger.error("Pipeline terminated with errors.")
