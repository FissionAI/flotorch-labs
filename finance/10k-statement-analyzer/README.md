# 10-K Statement Analyzer

**10-K Statement Analyzer** is an interactive GenAI-powered tool designed to query and analyze annual financial reports (10-K statements) of major tech companies using natural language. It integrates:

- **Amazon Bedrock Knowledge Base**, where 10-K filings (2022–2024) for Apple, Amazon, Google, Microsoft, Netflix, Intel, NVIDIA, and Tesla are indexed.
- **`Flotorch Core`**, FloTorch-core is a modular and extensible Python framework for building LLM-powered RAG (Retrieval-Augmented Generation) pipelines. It offers plug-and-play components for embeddings, chunking, retrieval, gateway-based LLM calls, and RAG evaluation.

Users can input a question and select up to three different Bedrock-supported LLMs to compare their generated responses side-by-side. The app utilizes Retrieval-Augmented Generation (RAG) to ensure responses are grounded in factual 10-K data.


## 🧠 Overview

- **Query 10-K Filings**: Ask natural language questions about financial statements.
- **Bedrock + flotorch-core**: Uses `flotorch-core` to fetch context from the Amazon Bedrock Knowledgebase and generate answers via  FloTorch LLM gateway with Bedrock as provider.
- **Compare LLMs**: Select and compare up to three different models side-by-side.

---

## 🏗️ Architecture

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Knowledge Base**: 10-K statements from 2022–2024 for Apple, Amazon, Google, Microsoft, Netflix, Intel, NVIDIA, and Tesla are indexed into Amazon Bedrock Knowledge Base.
- **Context Retrieval**: Retrieved from Bedrock KnowledgeBases using `flotorch-core` package.
- **LLM Inference**: Powered by `GatewayInferencer` from `flotorch-core` via Bedrock models.
```
┌─────────────┐         ┌─────────────┐         ┌────────────────┐
│  Streamlit  │  HTTP/  │   FastAPI   │         │   Bedrock KB   │
│  Frontend   │   REST  │   Backend   │ ◄──────►│ (flotorch-core)│
│             │ ◄─────► │             │         │                │
└─────────────┘         └─────────────┘         └────────────────┘
                              │
                              │
                              ▼
                        ┌─────────────────┐
                        │ GatewayInference│
                        │ (flotorch-core) │
                        │                 │
                        └─────────────────┘
```

## 🚀 Features

- Ask finance-related questions and get structured answers
- Compare up to 3 Bedrock-powered LLMs at once
- Transparent metadata including token usage and cost breakdown
- Uses Retrieval-Augmented Generation (RAG) for context-aware responses

---

## Configuration

Create a `.env` file in the root directory with the following environment variables:

```
ORIGINS='["http://localhost", "http://localhost:8003", "http://localhost:3000"]'
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
KNOWLEDGE_BASE_ID=your_bedrock_kb_id
BASE_URL= your_base_url
BEDROCK_REGION= us-east-1
API_KEY= flotorch_api_key
FASTAPI_SERVICE= http://localhost:8003
MODELS= list_of_llm_models_in_json_format
```

Make sure to replace the placeholder values with your actual credentials and configuration:

## ▶️ How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Backend

```bash
uvicorn run:app --port 8003
```

### Frontend

```bash
streamlit run frontend
```

---
