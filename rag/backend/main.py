from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from rag_service import RAGService
from typing import List
import os
from pydantic import BaseModel
import tempfile

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = RAGService()
rag_service.initialize()

class SearchQuery(BaseModel):
    query: str
    k: int = 4

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file.flush()
        
        # Process the file based on its extension
        file_type = "pdf" if file.filename.endswith(".pdf") else "text"
        rag_service.process_and_store_document(temp_file.name, file_type)
        
        # Clean up
        os.unlink(temp_file.name)
    
    return {"message": "Document processed successfully"}

@app.post("/api/search")
async def search_documents(query: SearchQuery):
    results = rag_service.search(query.query, query.k)
    return {
        "results": [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in results
        ]
    } 