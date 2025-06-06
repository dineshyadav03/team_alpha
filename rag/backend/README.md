# HSA Document RAG Backend

The backend service for the HSA Document RAG system, handling document processing, vector storage, and querying.

## 🛠️ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the `backend` directory:
```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX=your_pinecone_index_name
```

### 3. Pinecone Setup
1. Create a Pinecone account at [pinecone.io](https://pinecone.io)
2. Create a new index:
   - Name: `hsa-documents` (or your preferred name)
   - Dimension: `1536` (for OpenAI embeddings)
   - Metric: `cosine`
   - Environment: Choose the closest to your location (e.g., `gcp-starter`)

## 📁 Project Structure

```
backend/
├── dataset/                # HSA documents
│   ├── hsa_regulations/    # HSA regulations
│   └── medical_guidelines/ # Medical guidelines
├── document_processor.py   # Document processing logic
├── vector_store.py        # Vector storage interface
├── main.py               # FastAPI application
└── requirements.txt      # Python dependencies
```

## 🚀 Usage

### 1. Process Documents
```bash
python process_sample_docs.py
```

### 2. Start the Server
```bash
uvicorn main:app --reload
```

### 3. Query Documents
```bash
python query_documents.py
```

## 📚 API Endpoints

### Query Documents
```http
POST /api/query
Content-Type: application/json

{
    "query": "What are the HSA regulations for medical devices?",
    "filters": {
        "document_type": "regulation",
        "version": "1.0"
    }
}
```

### Process Documents
```http
POST /api/process
Content-Type: application/json

{
    "file_path": "path/to/document.pdf",
    "metadata": {
        "source": "HSA",
        "type": "regulation"
    }
}
```

## 🔧 Configuration

### Document Processing
- Chunk size: 1000 characters
- Chunk overlap: 200 characters
- Supported formats: PDF, TXT

### Vector Search
- Similarity threshold: 0.7
- Maximum results: 5
- Metadata filtering: Document type, version, source

## 📝 Notes

- The backend uses FastAPI for the API server
- Document processing is handled by LangChain
- Vector storage is managed by Pinecone
- OpenAI embeddings are used for vector generation 