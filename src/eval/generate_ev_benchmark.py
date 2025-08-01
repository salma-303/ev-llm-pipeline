# src/eval/generate_ev_benchmark.py

import os, json

BENCHMARK_PATH = "data/benchmark/ev_testset.jsonl"

BENCHMARK_QUESTIONS = [
    "What is ISO 15118 and why is it important for EV charging?",
    "Explain Plug & Charge in the context of EV charging.",
    "What are the charging modes defined by IEC 61851?",
    "How does V2G (Vehicle-to-Grid) functionality work?",
    "What safety standards apply to public EV chargers?",
    "What is the role of smart metering in EV charging?",
    "How do EVs authenticate themselves to chargers?",
    "Compare AC vs. DC charging for electric vehicles.",
    "What are the common communication protocols used in EVSE?",
    "Why is interoperability important in EV charging infrastructure?"
]

def save_benchmark():
    os.makedirs("data/benchmark", exist_ok=True)
    with open(BENCHMARK_PATH, "w", encoding="utf-8") as f:
        for q in BENCHMARK_QUESTIONS:
            json.dump({"instruction": q, "input": "", "output": ""}, f)
            f.write("\n")
    print(f"Benchmark test set saved to {BENCHMARK_PATH}")

if __name__ == "__main__":
    save_benchmark()
