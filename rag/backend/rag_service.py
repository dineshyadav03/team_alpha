from document_processor import DocumentProcessor
from vector_store import VectorStore
from langchain.schema import Document
from typing import List, Literal
import os
from dotenv import load_dotenv

load_dotenv()

class RAGService:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStore()

    def initialize(self):
        self.vector_store.initialize()

    def process_and_store_document(self, file_path: str, file_type: Literal["pdf", "text"]) -> None:
        if file_type == "pdf":
            documents = self.document_processor.process_pdf(file_path)
        else:
            documents = self.document_processor.process_text(file_path)
        
        self.vector_store.add_documents(documents)

    def search(self, query: str, k: int = 4) -> List[Document]:
        return self.vector_store.similarity_search(query, k) 