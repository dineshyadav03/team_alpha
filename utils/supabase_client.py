import os
from typing import List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv
import yaml

class SupabaseClient:
    def __init__(self, config_path: str = "../config.yaml"):
        """Initialize Supabase client with configuration."""
        load_dotenv()
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize Supabase client
        self.supabase: Client = create_client(
            os.getenv('SUPABASE_URL'),
            os.getenv('SUPABASE_KEY')
        )
        
        # Ensure tables exist
        self._create_tables_if_not_exist()

    def _create_tables_if_not_exist(self):
        """Create necessary tables if they don't exist."""
        # Create documents table
        self.supabase.table('documents').create({
            'id': 'uuid default uuid_generate_v4() primary key',
            'content': 'text not null',
            'metadata': 'jsonb not null',
            'embedding': 'vector(1536) not null',
            'created_at': 'timestamp with time zone default timezone(\'utc\'::text, now()) not null'
        }, if_not_exists=True)

    def store_embeddings(self, embedded_chunks: List[Dict[str, Any]]) -> None:
        """Store embedded chunks in Supabase."""
        for chunk in embedded_chunks:
            try:
                self.supabase.table('documents').insert({
                    'content': chunk['content'],
                    'metadata': chunk['metadata'],
                    'embedding': chunk['embedding']
                }).execute()
            except Exception as e:
                print(f"Error storing chunk: {str(e)}")

    def search_similar(self, query_embedding: List[float], 
                      limit: int = None,
                      similarity_threshold: float = None) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity."""
        if limit is None:
            limit = self.config['max_results']
        if similarity_threshold is None:
            similarity_threshold = self.config['similarity_threshold']

        try:
            # Perform vector similarity search
            response = self.supabase.rpc(
                'match_documents',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': similarity_threshold,
                    'match_count': limit
                }
            ).execute()

            return response.data
        except Exception as e:
            print(f"Error searching similar documents: {str(e)}")
            return []

    def filter_by_metadata(self, metadata_filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter documents by metadata fields."""
        try:
            query = self.supabase.table('documents').select('*')
            
            for key, value in metadata_filters.items():
                query = query.eq(f'metadata->{key}', value)
            
            response = query.execute()
            return response.data
        except Exception as e:
            print(f"Error filtering documents: {str(e)}")
            return []

if __name__ == "__main__":
    # Example usage
    from scripts.embedding_generator import EmbeddingGenerator
    
    # Initialize clients
    supabase = SupabaseClient()
    generator = EmbeddingGenerator()
    
    # Example search
    query = "What are the setback requirements for residential buildings?"
    query_embedding = generator.generate_embeddings([{'content': query}])[0]['embedding']
    
    # Search for similar documents
    results = supabase.search_similar(query_embedding)
    print(f"Found {len(results)} similar documents") 