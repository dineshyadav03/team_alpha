import os
from typing import List, Dict, Any
import openai
from dotenv import load_dotenv
import yaml
from tqdm import tqdm

class EmbeddingGenerator:
    def __init__(self, config_path: str = "../config.yaml"):
        """Initialize the embedding generator with configuration."""
        load_dotenv()
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.embedding_model = self.config['embedding_model']
        self.embedding_dimensions = self.config['embedding_dimensions']
        self.api_settings = self.config['api']
        
        # Initialize OpenAI client
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

    def generate_embeddings(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate embeddings for a list of text chunks."""
        embedded_chunks = []
        
        for chunk in tqdm(chunks, desc="Generating embeddings"):
            try:
                # Generate embedding for the chunk content
                response = openai.embeddings.create(
                    model=self.embedding_model,
                    input=chunk['content']
                )
                
                # Add embedding to chunk data
                embedded_chunk = {
                    'content': chunk['content'],
                    'metadata': chunk['metadata'],
                    'embedding': response.data[0].embedding
                }
                embedded_chunks.append(embedded_chunk)
                
            except Exception as e:
                print(f"Error generating embedding for chunk: {str(e)}")
                continue
        
        return embedded_chunks

    def batch_generate_embeddings(self, chunks: List[Dict[str, Any]], batch_size: int = 100) -> List[Dict[str, Any]]:
        """Generate embeddings in batches to handle rate limits."""
        all_embedded_chunks = []
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            embedded_batch = self.generate_embeddings(batch)
            all_embedded_chunks.extend(embedded_batch)
            
            # Add a small delay to respect rate limits
            if i + batch_size < len(chunks):
                import time
                time.sleep(1)  # 1 second delay between batches
        
        return all_embedded_chunks

if __name__ == "__main__":
    # Example usage
    from document_processor import DocumentProcessor
    
    # Process documents
    processor = DocumentProcessor()
    chunks = processor.process_directory("../data")
    
    # Generate embeddings
    generator = EmbeddingGenerator()
    embedded_chunks = generator.batch_generate_embeddings(chunks)
    
    print(f"Generated embeddings for {len(embedded_chunks)} chunks") 