# src/config_loader.py

import yaml
import logging

def load_config(path="config/config.yaml") -> dict:
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Failed to load config from {path}: {e}")
        raise
