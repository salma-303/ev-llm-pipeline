from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import time

class Query(BaseModel):
    prompt: str
    token: str  # Simple auth

API_TOKEN = "your_secret_token"

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
adapter_path = "models/llama3-8b-lora-v1"

tokenizer = AutoTokenizer.from_pretrained(model_id)
base_model = AutoModelForCausalLM.from_pretrained(
    model_id, torch_dtype=torch.float16, device_map="auto"
)
model = PeftModel.from_pretrained(base_model, adapter_path)
model.eval()

app = FastAPI()

@app.post("/generate")
async def generate(query: Query):
    if query.token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    inputs = tokenizer(f"### Instruction:\n{query.prompt}\n### Response:", return_tensors="pt").to("cuda")
    start = time.time()
    outputs = model.generate(**inputs, max_new_tokens=256)
    latency = time.time() - start

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {
        "output": result,
        "latency": round(latency, 3)
    }
