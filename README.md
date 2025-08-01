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
    - WandB integration for logging you can check it [here](https://wandb.ai/salmawaleed303-arab-academy-for-science-technology-marit/huggingface/runs/p4i7oaxz?nw=nwusersalmawaleed303)

- Output:
    - Adapter weights
    - Updated tokenizer
    - Logged metrics and checkpoints

### ✅ Step 6: Evaluation
- Domain-specific EV benchmark set (`ev_testset.jsonl`)
- Metrics:
  - ✅ BLEU (via `evaluate`)
  - ✅ ROUGE-L
  - ✅ Latency and throughput (tokens/sec)
- Comparison:
  - Base model vs. fine-tuned model

### ✅ Step 7: Deployment
- Model registered as versioned PEFT adapter
- API served via **FastAPI**: `src/api/inference_api.py`
- Token-based authentication
- Monitored latency via logs
- Docker-ready deployment

### ✅ Step 8: Orchestration & MLOps
- CLI scripts for automation
- Scheduled + manual triggers (GitHub Actions)
- CI/CD pipeline includes:
  - `pip install`, linting, and full pipeline execution
  - Model version control
  - Optional deployment step
## 🧪 Example API Usage

    ```http
    POST /generate
    Content-Type: application/json

    {
    "prompt": "Explain ISO 15118 and Plug & Charge.",
    "token": "your_secret_token"
    }```

    ```
    {
    "output": "ISO 15118 is a communication protocol that enables...",
    "latency": 2.17
    }
    ```
Run locally:
    ```
    uvicorn src.api.inference_api:app --port 8000 --reload
    ```
## Setup & Installation

### 1. Clone the Repo
    ```
    git clone https://github.com/your-username/ev-llm-pipeline.git
    cd ev-llm-pipeline
    ```
### 2. Install Dependencies
    ```
    pip install -r requirements.txt
    ```

### 3. Set up Environment Variables
    ```
    # .env
        GEMINI_API_KEY=your_key
        HUGGINGFACE_TOKEN=your_token
        WANDB_API_KEY=your_token
    ```
### 4. Run Pipeline End-to-End
    ```
    python src/main.py
    python src/main_qa.py
    python src/eval/benchmark_eval.py
    ```

## Prompting Strategy
Prompts follow this format:

    ```
    ### Instruction:
    What is ISO 15118?

    ### Response:
    ```

    - Long passages chunked into 512-token blocks
    - Each block passed to LLM to generate 10 QA pairs
    - Structured system prompt included via PromptManager




