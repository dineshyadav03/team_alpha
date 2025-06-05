# RECAP – Regulatory Compliance Assistant for Planning

A RAG-based AI assistant built for HSA (Hiten Sethi Associates) to help builders and architects with regulatory compliance in Maharashtra.

## 🎯 Objective

To build a **RAG-based AI assistant** that can help:

| User Type      | Key Function                                      |
| -------------- | ------------------------------------------------- |
| **Builders**   | Ask "What can I build here?" by location          |
| **Architects** | Ask "Is this plan compliant?" via document upload |

## 📍 Current Scope

| Parameter          | Value                                             |
| ------------------ | ------------------------------------------------- |
| **Firm**           | HSA (Hiten Sethi Associates)                      |
| **State Focus**    | Maharashtra                                       |
| **Document Types** | Zoning rules, DCR, parking, fire safety, setbacks |

## 🧠 Architecture Overview

This project uses a **Retrieval-Augmented Generation (RAG)** architecture.

| Layer                    | Tool/Service                                                                  | Notes                                                |
| ------------------------ | ----------------------------------------------------------------------------- | ---------------------------------------------------- |
| **Frontend**             | [Vercel AI SDK RAG Template](https://vercel.com/templates/next.js/ai-sdk-rag) | Built on Next.js with chat UI and OpenAI integration |
| **Backend**              | Node.js API Routes (via Vercel template)                                      | You can extend with custom endpoints                 |
| **Vector DB**            | Supabase with pgvector                                                        | Stores embeddings + metadata                         |
| **Embeddings**           | OpenAI (`text-embedding-ada-002`)                                             | Converts docs into vectors for search                |
| **LLM**                  | OpenAI GPT-4                                                                  | Generates summaries, compliance feedback             |
| **Chunking & Retrieval** | LangChain / LlamaIndex                                                        | Parses, chunks, tags metadata, and searches          |

## 📁 Project Structure

```
recap-regulatory-assistant/
│
├── /data/              ← Raw files from HSA (PDFs, PNGs)
├── /scripts/           ← Parsing + embedding logic
├── /rag/               ← RAG pipeline logic
├── /utils/             ← Supabase + metadata helper functions
├── config.yaml         ← Embedding/search configs
├── .env                ← Secrets (OpenAI + Supabase)
├── requirements.txt    ← Python dependencies
└── next.config.js      ← Vercel frontend config
```

## 🚀 Getting Started

1. Clone this repository
2. Install dependencies:
   ```bash
   npm install  # For frontend
   pip install -r requirements.txt  # For Python backend
   ```
3. Set up your environment variables in `.env`
4. Run the development server:
   ```bash
   npm run dev
   ```

## 🔐 Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=sk-xxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=service-role-key
EMBEDDING_MODEL=text-embedding-ada-002
```

## 📝 License

This project is proprietary and confidential. All rights reserved. 