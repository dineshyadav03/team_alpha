# HSA Document RAG System

A Retrieval-Augmented Generation (RAG) system for HSA (Health Sciences Authority) documents, built with LangChain, OpenAI, and Pinecone. This system enables intelligent document processing, storage, and querying for HSA regulations and medical guidelines.

## 🌟 Features

<<<<<<< HEAD
- **Document Processing**
  - Handles PDFs and text files
  - Advanced chunking and metadata extraction
  - Automatic embedding generation
=======
- 📝 Document Upload: Upload PDF and text documents about HSA and Maharashtra regulations
- 💬 AI Chat Interface: Ask questions about uploaded documents
- 🔍 Smart Search: Advanced document search using vector embeddings
- 🚀 Real-time Responses: Get instant answers to your queries

>>>>>>> 1c18ea8007583c289c1483fc0aeb37e7f829eab4

- **Vector Storage**
  - Uses Pinecone for efficient vector similarity search
  - Scalable and fast document retrieval
  - Metadata filtering support

- **Smart Retrieval**
  - Combines vector similarity with metadata filtering
  - Context-aware document search
  - Real-time query processing

- **Modern UI**
  - Clean, responsive interface built with Next.js
  - Real-time chat interface
  - Document upload and management

## 🛠️ Tech Stack

- **Backend**
  - Python 3.8+
  - FastAPI
  - LangChain
  - OpenAI Embeddings
  - Pinecone Vector Database

- **Frontend**
  - Next.js 14
  - React
  - TypeScript
  - Tailwind CSS

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key
- Pinecone account and API key

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd team_alpha
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd rag/backend
pip install -r requirements.txt
```

#### Configure Environment Variables
Create a `.env` file in `rag/backend/`:
```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX=your_pinecone_index_name
```

#### Set Up Pinecone
1. Create a Pinecone account at [pinecone.io](https://pinecone.io)
2. Create a new index:
   - Name: `hsa-documents` (or your preferred name)
   - Dimension: `1536` (for OpenAI embeddings)
   - Metric: `cosine`
   - Environment: Choose the closest to your location (e.g., `gcp-starter`)

### 3. Frontend Setup

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
│   │   ├── dataset/           # HSA documents
│   │   │   ├── hsa_regulations/    # HSA regulations
│   │   │   └── medical_guidelines/ # Medical guidelines
│   │   ├── document_processor.py   # Document processing logic
│   │   ├── vector_store.py        # Vector storage interface
│   │   └── main.py               # FastAPI application
│   └── frontend/
│       ├── app/                    # Next.js app directory
│       │   ├── api/               # API routes
│       │   └── page.tsx           # Main page
│       ├── components/            # React components
│       │   ├── DocumentUpload.tsx # Document upload component
│       │   └── ChatInterface.tsx  # Chat interface component
│       └── styles/               # Tailwind CSS styles
└── utils/
    └── pinecone_client.py     # Pinecone integration
```

## 🚀 Usage

### 1. Process Documents
```bash
cd rag/backend
python process_sample_docs.py
```

### 2. Start the Backend
```bash
cd rag/backend
uvicorn main:app --reload
```

### 3. Start the Frontend
```bash
cd frontend
npm run dev
```

### 4. Query Documents
- Use the web interface at `http://localhost:3000`
- Or use the Python script:
```bash
cd rag/backend
python query_documents.py
```

## 📚 API Documentation

### Backend API Endpoints

#### Query Documents
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

#### Process Documents
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

### Frontend Components
- `DocumentUpload`: Handles document uploads
- `ChatInterface`: Manages chat interactions
- `SearchResults`: Displays search results

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔍 Troubleshooting

### Common Issues

1. **Pinecone Connection Error**
   - Verify your API key and environment
   - Check if the index exists
   - Ensure the index dimension matches (1536)

2. **Document Processing Failures**
   - Check file format support
   - Verify file permissions
   - Check OpenAI API key

3. **Frontend Connection Issues**
   - Verify backend server is running
   - Check API URL configuration
   - Ensure CORS is properly configured

## 📞 Support

For support, please:
1. Check the troubleshooting guide
2. Open an issue in the GitHub repository
3. Contact the maintainers
