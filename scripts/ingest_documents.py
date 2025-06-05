import os
import argparse
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm

from document_processor import DocumentProcessor
from embedding_generator import EmbeddingGenerator
from utils.supabase_client import SupabaseClient

def ingest_documents(data_dir: str, batch_size: int = 100) -> None:
    """Main function to ingest documents into the system."""
    print("Starting document ingestion pipeline...")
    
    # Initialize components
    processor = DocumentProcessor()
    generator = EmbeddingGenerator()
    supabase = SupabaseClient()
    
    # Process documents
    print(f"\nProcessing documents from {data_dir}...")
    chunks = processor.process_directory(data_dir)
    print(f"Processed {len(chunks)} chunks from documents")
    
    # Generate embeddings
    print("\nGenerating embeddings...")
    embedded_chunks = generator.batch_generate_embeddings(chunks, batch_size)
    print(f"Generated embeddings for {len(embedded_chunks)} chunks")
    
    # Store in Supabase
    print("\nStoring chunks in Supabase...")
    supabase.store_embeddings(embedded_chunks)
    print("Ingestion complete!")

def main():
    parser = argparse.ArgumentParser(description='Ingest documents into the RAG system')
    parser.add_argument('--data-dir', type=str, default='../data',
                      help='Directory containing documents to process')
    parser.add_argument('--batch-size', type=int, default=100,
                      help='Batch size for embedding generation')
    
    args = parser.parse_args()
    
    # Ensure data directory exists
    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"Error: Data directory {data_dir} does not exist")
        return
    
    # Run ingestion
    ingest_documents(str(data_dir), args.batch_size)

if __name__ == "__main__":
    main() 