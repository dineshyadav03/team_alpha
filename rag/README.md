# RAG Implementation for HSA

This directory contains the Retrieval-Augmented Generation (RAG) implementation for HSA using a hybrid approach:
- Python backend for RAG processing
- TypeScript/Next.js frontend for the web interface

## Structure

### Backend (Python)
- `backend/document_processor.py`: Handles document processing for PDFs and text files
- `backend/vector_store.py`: Manages vector storage using Pinecone
- `backend/rag_service.py`: Main service that coordinates document processing and vector search
- `backend/main.py`: FastAPI server exposing the RAG functionality

### Frontend (TypeScript)
- `lib/api.ts`: API client for communicating with the Python backend
- Next.js components and pages for the web interface

## Setup

### Backend Setup
1. Create a Python virtual environment:
```bash
cd rag/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX=your_pinecone_index
```

4. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

### Frontend Setup
1. Install dependencies:
```bash
npm install
```

2. Set up environment variables in `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Start the Next.js development server:
```bash
npm run dev
```

## Usage

The system can be used to:
1. Upload and process documents (PDFs and text files)
2. Perform similarity search on stored documents
3. Generate responses using the retrieved context

Example usage from the frontend:
```typescript
import { uploadDocument, searchDocuments } from '../lib/api';

// Upload a document
await uploadDocument(file);

// Search for relevant documents
const results = await searchDocuments('your query here');
```

## Dependencies

### Backend
- langchain: For document processing and embeddings
- pinecone-client: For vector storage
- fastapi: For the API server
- openai: For embeddings and text generation

### Frontend
- next: React framework
- typescript: Type safety
- openai: For text generation 

# HSA Information Assistant - Backend

This directory contains the backend implementation for the HSA Information Assistant, handling document processing and vector storage.

## Features

- Document processing (PDF and text files)
- Vector embeddings generation
- Pinecone integration for vector storage
- FastAPI server for API endpoints

## Setup

1. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the `rag/backend` directory:
   ```
   OPENAI_API_KEY=your-openai-api-key
   PINECONE_API_KEY=your-pinecone-api-key
   PINECONE_ENVIRONMENT=your-pinecone-environment
   PINECONE_INDEX_NAME=your-index-name
   ```

4. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### POST /api/upload
Upload and process a document.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (PDF or text file)

**Response:**
```json
{
  "message": "Document processed successfully"
}
```

### POST /api/search
Search for similar documents.

**Request:**
- Method: POST
- Content-Type: application/json
- Body:
  ```json
  {
    "query": "your search query"
  }
  ```

**Response:**
```json
{
  "results": [
    {
      "text": "relevant text chunk",
      "score": 0.95,
      "metadata": {
        "documentId": "doc123",
        "page": 1
      }
    }
  ]
}
```

## Project Structure

```
rag/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   └── .env             # Environment variables
└── README.md            # This file
```

## Dependencies

- FastAPI: Web framework
- Uvicorn: ASGI server
- OpenAI: For embeddings generation
- Pinecone: Vector database
- PDF-Parse: PDF processing
- Python-dotenv: Environment variable management

## Development

1. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Run tests**
   ```bash
   pytest
   ```

3. **Code formatting**
   ```bash
   black .
   ```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License. 