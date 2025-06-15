import os
from typing import List, Dict, Any, Optional
from pinecone import Pinecone as _PineconeConnection  # Alias for the actual Pinecone client
from langchain_openai import OpenAIEmbeddings
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
        
        # Initialize Pinecone connection instance
        self.pinecone_connection = _PineconeConnection(api_key=self.api_key, environment=self.environment)
        
        # Get index
        if self.index_name not in self.pinecone_connection.list_indexes().names():
            raise ValueError(f"Index '{self.index_name}' not found. Please create it in Pinecone console.")
        
        self.index = self.pinecone_connection.Index(self.index_name)
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
                            'content': doc['content'], # Store raw content
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
                    'content': match.metadata.get('content', ''), # Retrieve raw content
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
        """
        Get the total number of documents in the index.
        """
        try:
            stats = self.index.describe_index_stats()
            # Assuming a single namespace or summing across all
            total_count = sum(namespace.vector_count for namespace in stats.namespaces.values())
            return total_count
        except Exception as e:
            logger.error(f"Error getting document count: {str(e)}")
            return 0

    def fetch_sample_vector(self, top_k: int = 1) -> Optional[Dict[str, Any]]:
        """
        Fetches a sample vector and its metadata from the index (if available).
        This is useful for debugging to see how data is stored.
        """
        try:
            # Perform a query with an empty vector to get some results, if any exist
            # This is a hacky way to get a sample if you don't know any IDs
            stats = self.index.describe_index_stats()
            if stats.total_vector_count == 0:
                logger.info("No vectors in the index to fetch.")
                return None
            
            # Query with a dummy vector to get nearest neighbors, assuming they exist
            dummy_embedding = self.embeddings.embed_query("sample query") # Generate a dummy embedding
            results = self.index.query(
                vector=dummy_embedding,
                top_k=top_k,
                include_metadata=True
            )
            if results.matches:
                sample_match = results.matches[0]
                logger.info(f"Sample vector ID: {sample_match.id}")
                logger.info(f"Sample vector score: {sample_match.score}")
                logger.info(f"Sample vector metadata: {sample_match.metadata}")
                return {
                    "id": sample_match.id,
                    "score": sample_match.score,
                    "metadata": sample_match.metadata
                }
            else:
                logger.info("No matches found for sample vector query.")
                return None
        except Exception as e:
            logger.error(f"Error fetching sample vector: {str(e)}")
            return None

if __name__ == "__main__":
    # Example usage
    client = PineconeClient()
    
    # Store example document (if not already done via process_sample_docs.py)
    # test_doc = {
    #     'content': 'This is a test document about HSA regulations.',
    #     'metadata': {
    #         'source': 'test',
    #         'type': 'regulation',
    #         'version': '1.0'
    #     }
    # }
    # client.store_documents([test_doc])
    
    # Fetch sample vector to debug content storage
    sample_vector_data = client.fetch_sample_vector()
    if sample_vector_data:
        print("\n--- Sample Vector Data from Pinecone ---")
        print(f"ID: {sample_vector_data['id']}")
        print(f"Score: {sample_vector_data['score']}")
        print(f"Metadata: {sample_vector_data['metadata']}")
        if 'text' in sample_vector_data['metadata']:
            print(f"Text Content (from 'text' key): {sample_vector_data['metadata']['text'][:200]}...")
        elif 'page_content' in sample_vector_data['metadata']:
            print(f"Text Content (from 'page_content' key): {sample_vector_data['metadata']['page_content'][:200]}...")
        elif 'content' in sample_vector_data['metadata']:
            print(f"Text Content (from 'content' key): {sample_vector_data['metadata']['content'][:200]}...")
        else:
            print("No common text content key found in metadata.")

    # Get document count
    count = client.get_document_count()
    print(f"Total documents in index: {count}") 