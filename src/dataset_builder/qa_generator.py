# src/dataset_builder/qa_generator.py

import os, logging, json
from dotenv import load_dotenv
from openai import OpenAI
from src.dataset_builder.prompt_manager import PromptManager
import re

class QAGenerator:
    def __init__(self, prompt_manager: PromptManager, config: dict):
        load_dotenv()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.prompt = prompt_manager

        api_env = config["deepseek_api"]["api_key_env"]
        api_key = os.getenv(api_env)
        if not api_key:
            self.logger.error(f"Environment variable '{api_env}' not found!")
            raise ValueError
        base_url = config["deepseek_api"]["base_url"]

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = config["deepseek_api"].get("model", "deepseek/deepseek-r1:free")
        self.logger.info(f"Initialized DeepSeek QAGenerator with model '{self.model}'")

    def generate_qa(self, context: str) -> list:
        system = self.prompt.system_prompt
        user = self.prompt.build_prompt(context)
        try:
            self.logger.debug(f"Sending prompt:\nSystem: {system}\nUser: {user}")
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                temperature=0.7,
                top_p=0.95,
                max_tokens=1024,
                frequency_penalty=0,
                presence_penalty=0
            )
            raw = resp.choices[0].message.content
            self.logger.info(f"Model output:\n{raw}")
            parsed = self.parse_output(raw)
            self.logger.info(f"Parsed {len(parsed)} QAs from model output.")
            return parsed
        except Exception as e:
            self.logger.error(f"DeepSeek generation failed: {e}")
            return []


    def parse_output(self, text: str) -> list:
        qas = []
        try:
            lines = text.strip().splitlines()
            current_q, current_a = "", ""
            # Regex to match Q1/Q2... and A1/A2... patterns
            q_pattern = re.compile(r'^\s*q\d*\s*[:.]', re.IGNORECASE)
            a_pattern = re.compile(r'^\s*a\d*\s*[:.]', re.IGNORECASE)
            
            for line in lines:
                if q_pattern.match(line):
                    if current_q and current_a:
                        qas.append({"question": current_q.strip(), "answer": current_a.strip()})
                    # Extract text after the Q prefix
                    parts = re.split(r'[:.]', line, 1)
                    current_q = parts[1].strip() if len(parts) > 1 else ""
                    current_a = ""
                elif a_pattern.match(line):
                    # Extract text after the A prefix
                    parts = re.split(r'[:.]', line, 1)
                    current_a = parts[1].strip() if len(parts) > 1 else ""
                elif current_a:
                    current_a += " " + line.strip()
                    
            if current_q and current_a:
                qas.append({"question": current_q.strip(), "answer": current_a.strip()})
                
        except Exception as e:
            self.logger.error(f"Failed to parse QA output: {e}")
        return qas