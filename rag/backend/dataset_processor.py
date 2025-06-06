from document_processor import DocumentProcessor
from vector_store import VectorStore
import os
from typing import List
from langchain.schema import Document
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetProcessor:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.dataset_path = os.path.join(os.path.dirname(__file__), "dataset")
        
    def initialize(self):
        """Initialize the vector store"""
        self.vector_store.initialize()
        
    def process_dataset(self):
        """Process all documents in the dataset directory and store them directly in Pinecone"""
        logger.info("Starting dataset processing...")
        
        # Process HSA regulations
        hsa_regs_path = os.path.join(self.dataset_path, "hsa_regulations")
        self._process_directory(hsa_regs_path)
        
        # Process medical guidelines
        guidelines_path = os.path.join(self.dataset_path, "medical_guidelines")
        self._process_directory(guidelines_path)
        
        logger.info("Dataset processing completed!")
        
    def _process_directory(self, directory: str):
        """Process all documents in a directory and store them directly in Pinecone"""
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(('.pdf', '.txt')):
                    file_path = os.path.join(root, file)
                    logger.info(f"Processing {file_path}")
                    
                    # Determine file type
                    file_type = "pdf" if file.endswith('.pdf') else "text"
                    
                    # Process and store document
                    if file_type == "pdf":
                        documents = self.document_processor.process_pdf(file_path)
                    else:
                        documents = self.document_processor.process_text(file_path)
                    
                    # Store in vector database
                    self.vector_store.add_documents(documents)
                    logger.info(f"Processed and stored {len(documents)} chunks from {file}")

if __name__ == "__main__":
    processor = DatasetProcessor()
    processor.initialize()
    processor.process_dataset() 