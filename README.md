# HSA Chatbot - RAG System

A complete Retrieval-Augmented Generation (RAG) system for HSA (Hiten Sethi & Associates) that enables intelligent document processing, storage, and conversational AI interactions. Built with FastAPI backend, Next.js frontend, OpenAI embeddings, and Pinecone vector database.

## 🌟 Features

### **Conversational AI**
- Natural language chat interface with document-aware responses
- Contextual answers based on uploaded documents
- Real-time conversation with AI that understands HSA's document context
- Intelligent responses combining general knowledge with specific document content

### **Document Processing**
- **User Upload**: Temporary document analysis (like ChatGPT) - documents are analyzed but not permanently stored
- **Admin Upload**: Permanent storage in Pinecone database with admin key authentication
- Supports PDF documents with automatic text extraction and chunking
- Advanced metadata extraction and embedding generation
- Bulk upload utilities for multiple documents

### **Vector Storage & Search**
- Pinecone vector database for efficient similarity search
- OpenAI embeddings (1536 dimensions) for high-quality document representation
- Smart retrieval combining vector similarity with contextual understanding
- Currently indexed: Maharashtra Fire Prevention and Life Safety Act 2006 (134 document chunks)

### **Modern Web Interface**
- Clean, responsive chat interface built with Next.js and Tailwind CSS
- Real-time messaging with typing indicators
- Document upload with drag-and-drop support
- Mobile-friendly design

## 🛠️ Tech Stack

### **Backend**
- **FastAPI** - Modern Python web framework
- **OpenAI API** - GPT models and embeddings
- **Pinecone** - Vector database for document storage
- **LangChain** - Document processing and text splitting
- **Python 3.8+** with comprehensive dependencies

### **Frontend**
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **React** - Component-based UI

### **Infrastructure**
- **CORS-enabled API** for frontend-backend communication
- **Environment-based configuration** for secure API key management
- **Modular architecture** with separate services for different functionalities

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys))
- **Pinecone account and API key** ([Sign up here](https://www.pinecone.io/))

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
```

#### Configure Environment Variables
Create a `.env` file in `rag/backend/`:
```env
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=hsa-documents
ADMIN_UPLOAD_KEY=your_secure_admin_key_here
```

#### Set Up Pinecone Index
1. Go to [Pinecone Console](https://app.pinecone.io)
2. Create a new index:
   - **Name**: `hsa-documents`
   - **Dimension**: `1536` (for OpenAI embeddings)
   - **Metric**: `cosine`
   - **Cloud**: `AWS`
   - **Region**: `us-east-1`

#### Start the Backend Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Backend will be available at: `http://localhost:8000`

### 3. Frontend Setup

#### Install Dependencies
```bash
cd rag/frontend
npm install
```

#### Start the Frontend
```bash
npm run dev
```
Frontend will be available at: `http://localhost:3000`

## 📁 Project Structure

```
team_alpha/
├── rag/
│   ├── backend/                    # FastAPI Backend
│   │   ├── main.py                # Main FastAPI application
│   │   ├── rag_service.py         # Core RAG functionality
│   │   ├── vector_store.py        # Pinecone vector operations
│   │   ├── document_processor.py  # PDF processing and chunking
│   │   ├── pinecone_client.py     # Pinecone client wrapper
│   │   ├── test_system.py         # System testing utilities
│   │   ├── requirements.txt       # Python dependencies
│   │   ├── dataset/               # Sample documents
│   │   │   ├── regulatory_compliance/
│   │   │   ├── design_documents/
│   │   │   └── project_management/
│   │   └── .env                   # Environment variables (create this)
│   │
│   └── frontend/                   # Next.js Frontend
│       ├── app/
│       │   ├── page.tsx           # Main chat interface
│       │   ├── layout.tsx         # App layout
│       │   ├── globals.css        # Global styles
│       │   └── api/               # API routes
│       │       ├── chat/route.ts  # Chat endpoint
│       │       └── upload/route.ts # Upload endpoint
│       ├── components/
│       │   ├── ChatInterface.tsx  # Main chat component
│       │   ├── DocumentUpload.tsx # Upload component
│       │   └── ui/                # UI components
│       ├── lib/
│       │   └── api.ts            # API configuration
│       ├── package.json          # Node.js dependencies
│       └── tailwind.config.ts    # Tailwind configuration
│
├── lib/                           # Shared utilities
│   ├── ai/embedding.ts           # AI embedding functions
│   ├── db/                       # Database schema
│   ├── actions/                  # Server actions
│   └── utils.ts                  # Utility functions
│
└── README.md                     # This file
```

## 🚀 Usage

### Chat Interface
1. Open `http://localhost:3000` in your browser
2. Start chatting with the HSA Chatbot
3. Ask questions about fire safety regulations, building codes, or general topics
4. The AI will provide contextual responses based on uploaded documents

### Document Upload

#### User Upload (Temporary Analysis)
1. Use the upload interface in the chat
2. Upload PDF documents for temporary analysis
3. Documents are processed but not permanently stored

#### Admin Upload (Permanent Storage)
1. Use the admin upload endpoint with your admin key
2. Documents are permanently stored in Pinecone
3. Becomes part of the searchable knowledge base

### Bulk Document Processing
```bash
cd rag/backend
python process_sample_docs.py  # Process sample documents
python test_system.py          # Run system tests
```

## 📚 API Endpoints

### Chat Endpoint
```
POST /api/chat
Content-Type: application/json

{
  "message": "What are the fire safety requirements for buildings?"
}
```

### User Upload (Temporary)
```
POST /api/upload
Content-Type: multipart/form-data

file: [PDF file]
```

### Admin Upload (Permanent)
```
POST /api/admin/upload
Content-Type: multipart/form-data
Authorization: Bearer your_admin_key

file: [PDF file]
```

### Health Check
```
GET /health
```

## 🔧 Configuration

### Backend Configuration (`.env`)
```env
# Required
OPENAI_API_KEY=sk-...                    # OpenAI API key
PINECONE_API_KEY=...                     # Pinecone API key
PINECONE_INDEX_NAME=hsa-documents        # Pinecone index name

# Optional
ADMIN_UPLOAD_KEY=secure_admin_key        # Admin upload authentication
PORT=8000                                # Server port
```

### Frontend Configuration
The frontend automatically connects to the backend at `http://localhost:8000`. No additional configuration needed for local development.

## 🧪 Testing

### Run Backend Tests
```bash
cd rag/backend
python test_system.py
```

### Test Document Processing
```bash
cd rag/backend
python process_sample_docs.py
```

### Test Pinecone Connection
```bash
cd rag/backend
python debug_pinecone_connection.py
```

## 🎯 Current System Status

### ✅ **Fully Implemented**
- Conversational AI with document context
- PDF upload and processing
- Vector storage and retrieval
- Web-based chat interface
- Admin and user upload modes
- CORS-enabled API

### 📊 **Current Data**
- **134 document chunks** from Maharashtra Fire Prevention and Life Safety Act 2006
- **Indexed in Pinecone** with OpenAI embeddings
- **Searchable knowledge base** for fire safety regulations

### 🔄 **Recent Updates**
- Fixed frontend-backend communication
- Implemented dual upload modes
- Added comprehensive error handling
- Updated UI for better user experience

## 🔍 Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check dependencies
pip install -r requirements.txt

# Verify environment variables
cat .env

# Check port availability
lsof -i :8000  # On Unix systems
```

#### Frontend Connection Issues
```bash
# Ensure backend is running
curl http://localhost:8000/health

# Check frontend configuration
cd rag/frontend
npm run dev
```

#### Pinecone Connection Errors
1. Verify API key in `.env` file
2. Check index name matches exactly
3. Ensure index dimension is 1536
4. Run `python debug_pinecone_connection.py`

#### Upload Issues
1. Check file size limits
2. Verify PDF format
3. Ensure admin key is correct (for admin uploads)
4. Check backend logs for specific errors

### Getting Help
1. Check the console logs for specific error messages
2. Verify all environment variables are set correctly
3. Ensure all dependencies are installed
4. Test individual components using the provided test scripts

## 📞 Support

For issues or questions:
1. Check this troubleshooting guide
2. Review the console logs for specific errors
3. Open an issue on the GitHub repository
4. Ensure all prerequisites are properly configured

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for HSA (Hiten Sethi & Associates)**
