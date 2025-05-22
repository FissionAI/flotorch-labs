# 🧪 Ground Truth Preprocessor for Code Evaluation Datasets

This utility script loads a Hugging Face dataset (e.g., [OpenAI HumanEval](https://huggingface.co/datasets/openai_humaneval)), extracts question and answer fields, and saves them in a structured JSON format (`ground_truth.json`). It is primarily used for preparing datasets for LLM-based code generation evaluation pipelines.

---

## 📂 What It Does

* Loads a dataset from the Hugging Face Hub using the `datasets` library
* Allows configuration of question and answer fields via a `config.yml`
* Optionally uses an HF token for private datasets
* Saves a JSON file with each example formatted as:

  ```json
  {
    "question": "...",
    "answer": "..."
  }
  ```

---


## ⚙️ Configuration

Create a `config.yml` file in the project root with the following structure:

```yaml
DATASET_NAME: "your_dataset_name"
DATASET_CONFIG: "your_optional_config_name"  # (optional)
HF_TOKEN: "your_huggingface_token"           # (optional if dataset is public)
QUESTION_FIELDS: ["field1", "field2"]
ANSWER_FIELDS: ["field3"]
``` 

Example:

DATASET_NAME: "openai/codegen-eval"
DATASET_CONFIG: "default"
HF_TOKEN: "hf_abc123..."
QUESTION_FIELDS: ["prompt"]
ANSWER_FIELDS: ["solution"]


---

## ▶️ How to Run

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the script**

   ```bash
   python Flotorch_dataset_utility.py
   ```

3. **Output**

   * Saves processed JSON file to:

     ```
     data/ground_truth/ground_truth.json
     ```

---

## 📁 Example Output (1 Entry)

```json
{
  "question": "Write a function that returns the sum of two numbers.",
  "answer": "def add(a, b):\n    return a + b"
}
```

---

## 🛠️ Notes

* If the dataset does not contain a `train` split, all available splits will be processed.

---