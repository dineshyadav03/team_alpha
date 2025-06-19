# HSA Document RAG System

A Retrieval-Augmented Generation (RAG) system for HSA (Hiten Sethi & Associates) architectural documents, built with LangChain, OpenAI, and Pinecone. This system enables intelligent document processing, storage, and querying for HSA's various architectural and project management documents.

## 🌟 Features

- **Document Processing**
  - Handles PDF and text documents
  - Advanced chunking and metadata extraction
  - Automatic embedding generation
  - Supports diverse document types (Architectural Drawings, Regulations, Project Schedules, etc.)

- **Vector Storage**
  - Utilizes Pinecone for efficient high-dimensional vector similarity search
  - Scalable and fast document retrieval
  - Supports advanced metadata filtering for precise search
  - Direct upsert mechanism for robust data ingestion

- **Smart Retrieval**
  - Combines vector similarity with metadata filtering for highly relevant results
  - Context-aware document search for accurate responses
  - Designed for real-time query processing

- **Modern UI** (Frontend part, if applicable and implemented)
  - Clean, responsive interface built with Next.js and Tailwind CSS
  - Real-time chat interface for natural language interaction
  - Document upload and management capabilities

## 🛠️ Tech Stack

- **Backend**
  - Python 3.8+
  - FastAPI
  - LangChain (for document loading and splitting)
  - OpenAI Embeddings (for text vectorization)
  - Pinecone Vector Database (for vector storage and search)
  - `python-dotenv` (for environment variable management)

- **Frontend** (If applicable)
  - Next.js 14
  - React
  - TypeScript
  - Tailwind CSS

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend development)
- OpenAI API key
- Pinecone account and API key

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/dineshyadav03/team_alpha.git
cd team_alpha
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd rag/backend
pip install -r requirements.txt
# Also install specific packages that might be missing from requirements.txt
pip install pinecone langchain-openai langchain-community
```

#### Configure Environment Variables
Create a `.env` file in `rag/backend/` and populate it with your credentials:
```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1  # Based on your Pinecone console image
PINECONE_INDEX=hsa-documents
PORT=3000
NODE_ENV=development
```

#### Set Up Pinecone Index
1. Go to [Pinecone Console](https://app.pinecone.io)
2. Create a new index with these specifications:
   * Name: `hsa-documents`
   * Dimension: `1536` (required for OpenAI embeddings)
   * Metric: `cosine`
   * Capacity Mode: `Serverless`
   * Region: `us-east-1`
   * Deletion Protection: (Recommended to enable)

### 3. Frontend Setup (If applicable)

#### Install Node.js Dependencies
```bash
cd frontend
npm install
```

#### Configure Environment Variables
Create a `.env.local` file in `frontend/`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📁 Project Structure

```
team_alpha/
├── rag/
│   ├── backend/
│   │   ├── dataset/           # Raw HSA documents (Architectural, Regulatory, Project Management etc.)
│   │   │   ├── design_documents/
│   │   │   ├── regulatory_compliance/
│   │   │   └── project_management/
│   │   ├── document_processor.py   # Handles document loading, chunking, and metadata extraction
│   │   ├── vector_store.py        # Manages Pinecone interaction (embedding, upsert, search)
│   │   ├── debug_pinecone_connection.py # Script for direct Pinecone connection debugging
│   │   ├── pinecone_client.py     # Custom Pinecone client wrapper
│   │   ├── dataset_processor.py   # Orchestrates processing of local dataset documents
│   │   ├── process_sample_docs.py # Script to process sample documents for the index
│   │   ├── query_documents.py     # Script for testing document querying
│   │   ├── main.py               # FastAPI application entry point
│   │   ├── rag_service.py         # Core RAG logic
│   │   ├── requirements.txt      # Python dependencies
│   │   └── .env                   # Environment variables for backend (ignored by Git)
│   └── frontend/ (If applicable)
│       ├── app/                    # Next.js app directory
│       ├── components/            # React components
│       └── styles/               # Tailwind CSS styles
└── .gitignore                   # Specifies files/folders to ignore in Git
```

## 🚀 Usage

### 1. Process Documents
Navigate to the `rag/backend` directory and run the processing script. This will read your sample documents, convert them into embeddings, and upload them to your Pinecone index.
```bash
cd rag/backend
python process_sample_docs.py
```

### 2. Verify Documents in Pinecone (Optional)
To confirm documents were added to Pinecone and inspect their metadata:
```bash
cd rag/backend
python debug_pinecone_connection.py
```

### 3. Start the Backend API Server
```bash
cd rag/backend
uvicorn main:app --reload
```

### 4. Start the Frontend (If applicable)
```bash
cd frontend
npm run dev
```

### 5. Query Documents
- Use the web interface (if frontend is running, typically at `http://localhost:3000`)
- Or use the Python script to test queries directly:
```bash
cd rag/backend
python query_documents.py
```

## 📚 API Documentation (Backend Endpoints)

### Query Documents
`POST /api/query`
Content-Type: `application/json`

```json
{
    "query": "What are the main features of the NMMC Headquarters floor plan?",
    "filters": {
        "category": "design_documents",
        "subcategory": "architectural_drawings"
    }
}
```

### Process Documents
`POST /api/process`
Content-Type: `application/json`

```json
{
    "file_path": "path/to/document.pdf",
    "metadata": {
        "source": "HSA-Firm",
        "type": "architectural_drawing"
    }
}
```

## 🔧 Configuration

### Document Processing
- Chunk size: 1000 characters
- Chunk overlap: 200 characters
- Supported formats: PDF, TXT

### Vector Search
- Embedding Dimension: 1536 (for OpenAI embeddings)
- Metric: Cosine Similarity
- Similarity threshold: 0.7 (can be adjusted in `query_documents.py` or service logic)
- Maximum results: 5 (can be adjusted in `query_documents.py` or service logic)
- Metadata filtering: Customizable based on fields like `document_type`, `version`, `source`, `category`, `subcategory`, `project_name`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Commit your changes (`git commit -m "feat: Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature-name`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔍 Troubleshooting

### Common Issues

1. **Pinecone Connection Errors / No Vectors Detected in Index**
   * **Verify `.env` file:** Ensure `PINECONE_API_KEY`, `PINECONE_ENVIRONMENT` (`us-east-1`), and `PINECONE_INDEX` (`hsa-documents`) are *exactly* correct in `rag/backend/.env`. No extra spaces or incorrect characters.
   * **Recreate Pinecone Index:** If persistent issues, try deleting and recreating your `hsa-documents` index directly in the [Pinecone Console](https://app.pinecone.io) with the correct `1536` dimension and `cosine` metric.
   * **Run `debug_pinecone_connection.py`:** This script performs a direct, isolated test of your Pinecone connection and upsert. Its logs are critical for pinpointing issues.

2. **Document Processing Failures**
   * Check for `ModuleNotFoundError` and ensure all dependencies in `requirements.txt` (and those installed manually like `pinecone`, `langchain-openai`, `langchain-community`) are installed.
   * Verify file paths and permissions for documents in `rag/backend/dataset/`.
   * Ensure your `OPENAI_API_KEY` is correctly set in `.env`.

3. **Frontend Connection Issues**
   * Verify the backend server (`uvicorn main:app --reload`) is running.
   * Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`.
   * Ensure CORS is properly configured on the backend (FastAPI typically handles this).

### Still Stuck?

1. Double-check all environment variable values against your cloud provider consoles.
2. Clear Python cache: `python -m py_compile --clear-cache` (or delete `__pycache__` folders).
3. Provide full console output of errors when seeking support.

## 📞 Support

For support, please:
1. Check the troubleshooting guide above.
2. Open an issue in the GitHub repository.
3. Contact the maintainers (if specified in the project).
