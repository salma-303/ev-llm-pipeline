# finetune/training/prepare_data.py

import json

def convert_to_alpaca(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile:
        data = [json.loads(line) for line in infile]

    alpaca_format = []
    for item in data:
        alpaca_format.append({
            "instruction": item["question"],
            "input": "",
            "output": item["answer"]
        })

    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(alpaca_format, out, indent=2)

if __name__ == "__main__":
    convert_to_alpaca("data/qa_dataset.jsonl", "finetune/dataset/qa_dataset_alpaca.json")
