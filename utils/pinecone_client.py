import os
from typing import List, Dict, Any, Optional
import pinecone
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PineconeClient:
    def __init__(self):
        """Initialize Pinecone client with configuration."""
        load_dotenv()
        
        # Get environment variables
        self.api_key = os.getenv('PINECONE_API_KEY')
        self.environment = os.getenv('PINECONE_ENVIRONMENT')
        self.index_name = os.getenv('PINECONE_INDEX')
        
        if not all([self.api_key, self.environment, self.index_name]):
            raise ValueError("Missing Pinecone environment variables. Please check your .env file.")
        
        # Initialize Pinecone
        pinecone.init(api_key=self.api_key, environment=self.environment)
        
        # Get index
        if self.index_name not in pinecone.list_indexes():
            raise ValueError(f"Index '{self.index_name}' not found. Please create it in Pinecone console.")
        
        self.index = pinecone.Index(self.index_name)
        self.embeddings = OpenAIEmbeddings()
        
        logger.info(f"Pinecone client initialized with index: {self.index_name}")

    def store_documents(self, documents: List[Dict[str, Any]], batch_size: int = 100) -> None:
        """
        Store document chunks in Pinecone.
        
        Args:
            documents: List of dictionaries containing 'content', 'metadata', and optionally 'id'
            batch_size: Number of documents to process in each batch
        """
        try:
            # Process documents in batches
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                
                # Generate embeddings for the batch
                texts = [doc['content'] for doc in batch]
                embeddings = self.embeddings.embed_documents(texts)
                
                # Prepare vectors for upsert
                vectors = []
                for doc, embedding in zip(batch, embeddings):
                    vector = {
                        'id': doc.get('id', f"doc_{i}_{len(vectors)}"),
                        'values': embedding,
                        'metadata': {
                            'content': doc['content'],
                            **doc.get('metadata', {})
                        }
                    }
                    vectors.append(vector)
                
                # Upsert to Pinecone
                self.index.upsert(vectors=vectors)
                logger.info(f"Stored {len(vectors)} documents in Pinecone")
                
        except Exception as e:
            logger.error(f"Error storing documents in Pinecone: {str(e)}")
            raise

    def search_similar(self, 
                      query: str, 
                      top_k: int = 5, 
                      filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for similar documents using vector similarity.
        
        Args:
            query: The search query
            top_k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of similar documents with their metadata
        """
        try:
            # Generate embedding for the query
            query_embedding = self.embeddings.embed_query(query)
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter
            )
            
            # Format results
            documents = []
            for match in results.matches:
                documents.append({
                    'id': match.id,
                    'score': match.score,
                    'content': match.metadata.get('content', ''),
                    'metadata': {k: v for k, v in match.metadata.items() if k != 'content'}
                })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error searching similar documents: {str(e)}")
            return []

    def delete_documents(self, ids: List[str]) -> None:
        """
        Delete documents from Pinecone by their IDs.
        
        Args:
            ids: List of document IDs to delete
        """
        try:
            self.index.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents from Pinecone")
        except Exception as e:
            logger.error(f"Error deleting documents: {str(e)}")
            raise

    def get_document_count(self) -> int:
        """Get the total number of documents in the index."""
        try:
            stats = self.index.describe_index_stats()
            return stats.total_vector_count
        except Exception as e:
            logger.error(f"Error getting document count: {str(e)}")
            return 0

if __name__ == "__main__":
    # Example usage
    client = PineconeClient()
    
    # Example document
    test_doc = {
        'content': 'This is a test document about HSA regulations.',
        'metadata': {
            'source': 'test',
            'type': 'regulation',
            'version': '1.0'
        }
    }
    
    # Store document
    client.store_documents([test_doc])
    
    # Search for similar documents
    results = client.search_similar("HSA regulations")
    print(f"Found {len(results)} similar documents")
    
    # Get document count
    count = client.get_document_count()
    print(f"Total documents in index: {count}") 