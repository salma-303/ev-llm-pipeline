#  EV-LLM-Pipeline: Question-Answering Assistant for Electric Vehicle Charging Infrastructure

This project builds an end-to-end fine-tuning pipeline for a domain-specific LLM assistant focused on **Electric Vehicle (EV) charging infrastructure**. It leverages state-of-the-art language models, dataset generation, and memory-efficient fine-tuning techniques to produce a high-quality QA model.

---



## Pipeline Stages 

### ✅ 1. Data Collection
- Sources: Web scraping + PDF extraction
- Extracted from: NITI Aayog handbook, DOT climate strategy, ISO/IEC standards
- Output: Raw `.txt` files and metadata CSV

### ✅ 2. Data Processing
- Cleaning, deduplication, tokenization
- Normalization and formatting
- Exported as processed `.jsonl` blocks

### ✅ 3. QA Dataset Generation
- Used DeepSeek/Gemini/OpenRouter APIs
- System + user prompt format
- Generated Alpaca-style QA pairs:
  ```json
  {
    "instruction": "What is ISO 15118?",
    "input": "",
    "output": "ISO 15118 is a communication protocol for EV-to-charger interoperability..."
  }

### ✅ 4. Fine-tuning Preparation
- Converted QA pairs to instruction-tuned format
- Trained on Kaggle GPU (T4) using QLoRA and PEFT
- Model: meta-llama/Meta-Llama-3-8B-Instruct
- Saved to /Models/llama3-8b-lora

### ✅ 5. Fine-tuning
- Hugging Face Trainer with:
    - transformers, datasets, bitsandbytes, peft
    - Gradient accumulation and FP16
    - WandB integration for logging

- Output:
    - Adapter weights
    - Updated tokenizer
    - Logged metrics and checkpoints


