# src/dataset_builder/prompt_manager.py

import os
import logging

class PromptManager:
    def __init__(self, system_prompt_path="prompts/system_prompt.txt", qa_prompt_path="prompts/qa_instruction.txt"):
        self.logger = logging.getLogger(__name__)
        try:
            with open(system_prompt_path, "r", encoding="utf-8") as f:
                self.system_prompt = f.read()
            with open(qa_prompt_path, "r", encoding="utf-8") as f:
                self.qa_template = f.read()
        except Exception as e:
            self.logger.error(f"Failed to load prompts: {e}")
            raise

    def build_prompt(self, context: str) -> str:
        return self.qa_template.replace("{context}", context.strip())
