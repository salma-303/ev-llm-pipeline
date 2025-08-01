# src/eval/benchmark_eval.py

import os, json, time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import evaluate

BLEU = evaluate.load("bleu")
ROUGE = evaluate.load("rouge")

def load_testset(path="data/benchmark/ev_testset.jsonl"):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def generate_answer(model, tokenizer, prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    start = time.time()
    outputs = model.generate(**inputs, max_new_tokens=256)
    latency = time.time() - start
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded, latency, outputs[0].shape[-1]

def evaluate_model(model_id, adapter_dir=None, device="cuda" if torch.cuda.is_available() else "cpu"):
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto" if "cuda" in device else None,
        torch_dtype=torch.float16 if "cuda" in device else torch.float32,
        use_auth_token=True
    )

    if adapter_dir:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, adapter_dir)

    model.eval()
    testset = load_testset()
    preds, refs, latencies, tokens = [], [], [], []

    for ex in testset:
        prompt = f"### Instruction:\n{ex['instruction']}\n\n### Response:"
        output, latency, tok = generate_answer(model, tokenizer, prompt)
        preds.append(output.strip())
        refs.append([ex['output'].strip() or ""])
        latencies.append(latency)
        tokens.append(tok)

    print("\nEvaluation Results:")
    print(f"Avg Latency: {sum(latencies)/len(latencies):.2f}s")
    print(f"Avg Throughput: {sum(tokens)/sum(latencies):.2f} tokens/sec")

    BLEU_res = BLEU.compute(predictions=preds, references=refs)
    ROUGE_res = ROUGE.compute(predictions=preds, references=[r[0] for r in refs], use_stemmer=True)

    print(f"BLEU: {BLEU_res['bleu']:.4f}")
    print(f"ROUGE-L: {ROUGE_res['rougeL'].mid.fmeasure:.4f}")

if __name__ == "__main__":
    print("Evaluating Fine-Tuned Model")
    evaluate_model(
        model_id="meta-llama/Meta-Llama-3-8B-Instruct",
        adapter_dir="models/llama3-8b-lora"
    )

    print("\nEvaluating Baseline Model")
    evaluate_model(
        model_id="meta-llama/Meta-Llama-3-8B-Instruct",
        adapter_dir=None
    )
