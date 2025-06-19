from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from document_processor import DocumentProcessor
from dataset_processor import DatasetProcessor
from vector_store import VectorStore
import uvicorn
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

app = FastAPI(title="HSA RAG API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
document_processor = DocumentProcessor()
dataset_processor = DatasetProcessor()
vector_store = VectorStore()

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    try:
        vector_store.initialize()
        logger.info("Vector store initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {str(e)}")
        raise

@app.post("/api/chat")
async def chat(message: str):
    """Handle chat messages"""
    try:
        # Query the vector store
        results = vector_store.query(message)
        
        # Process results and generate response
        response = {
            "response": "Based on the HSA regulations, " + results[0]["content"] if results else "I couldn't find relevant information in the documents.",
            "sources": [r["metadata"]["source"] for r in results[:3]] if results else []
        }
        
        return response
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file uploads"""
    try:
        # Save the uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process the file
        if file.filename.lower().endswith('.pdf'):
            docs = document_processor.process_pdf(temp_path)
        else:
            docs = document_processor.process_text(temp_path)
        
        # Add to vector store
        vector_store.add_documents(docs)
        
        # Clean up
        os.remove(temp_path)
        
        return {"message": f"Successfully processed {file.filename}"}
    except Exception as e:
        logger.error(f"Error in upload endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
async def search(query: str):
    """Handle search queries"""
    try:
        results = vector_store.query(query)
        return {
            "results": [
                {
                    "content": r["content"],
                    "source": r["metadata"]["source"],
                    "score": r["score"]
                }
                for r in results
            ]
        }
    except Exception as e:
        logger.error(f"Error in search endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 