# src/main_qa.py

import logging
import os
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.dataset_builder.prompt_manager import PromptManager
from src.dataset_builder.qa_generator import QAGenerator
from src.config_loader import load_config

def setup_logger():
    logger = logging.getLogger("QAPipeline")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def build_qa_dataset(input_dir="data/processed", output_path="data/qa_dataset.jsonl"):
    logger = setup_logger()
    logger.info("Starting QA generation...")

    config = load_config("config/config.yaml")
    input_dir = config["qa_generation"]["input_dir"]
    output_path = config["qa_generation"]["output_file"]

    prompt_mgr = PromptManager()
    generator = QAGenerator(prompt_mgr, config)

    with open(output_path, "w", encoding="utf-8") as out_f:
        for file in os.listdir(input_dir):
            if not file.endswith(".jsonl"):
                continue
            try:
                with open(os.path.join(input_dir, file), "r", encoding="utf-8") as f:
                    for line in f:
                        block = json.loads(line)
                        qas = generator.generate_qa(block["text"])
                        if not qas:
                            logger.warning(f"No QA generated for block: {block.get('id', '[unknown]')}")

                        for qa in qas:
                            json.dump(qa, out_f)
                            out_f.write("\n")
                logger.info(f"QA generated from: {file}")
            except Exception as e:
                logger.error(f"Failed to process {file}: {e}")

if __name__ == "__main__":
    build_qa_dataset()
