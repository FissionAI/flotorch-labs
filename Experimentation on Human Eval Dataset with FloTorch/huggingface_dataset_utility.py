import json
import os
import yaml
from datasets import load_dataset

# Load YAML config
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

dataset_name = config.get("DATASET_NAME")
config_name = config.get("DATASET_CONFIG")
hf_token = config.get("HF_TOKEN")
question_fields = config.get("QUESTION_FIELDS", [])
answer_fields = config.get("ANSWER_FIELDS", [])

# Function to process dataset and save ground truth
def load_and_save_ground_truth():
    if config_name:
        dataset = load_dataset(dataset_name, config_name, token=hf_token) if hf_token else load_dataset(dataset_name, config_name)
    else:
        dataset = load_dataset(dataset_name, token=hf_token) if hf_token else load_dataset(dataset_name)

    splits_to_process = ["train"] if "train" in dataset else list(dataset.keys())

    def map_to_combined_fields(example):
        example["question"] = " ".join([example.get(field, "") for field in question_fields])
        example["answer"] = " ".join([example.get(field, "") for field in answer_fields])
        return example

    output_dir = os.path.join("data", "ground_truth")
    os.makedirs(output_dir, exist_ok=True)

    for split in splits_to_process:
        split_dataset = dataset[split].map(map_to_combined_fields)
        split_list = [{"question": e["question"], "answer": e["answer"]} for e in split_dataset]

        output_file = os.path.join(output_dir, f"ground_truth.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(split_list, f, indent=4, ensure_ascii=False)

        print(f"✅ Saved {split} split to {output_file}")
