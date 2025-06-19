import os
from typing import List, Dict, Any, Optional
from pinecone import Pinecone
from openai import OpenAI
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PineconeClient:
    def __init__(self):
        """Initialize Pinecone client with configuration."""
        load_dotenv()
        
        # Pinecone configuration
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.environment = os.getenv("PINECONE_ENVIRONMENT")
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        
        # OpenAI configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        if not all([self.api_key, self.environment, self.index_name, self.openai_api_key]):
            raise ValueError("Missing required environment variables")

    def initialize(self):
        """Initialize Pinecone client and create index if it doesn't exist"""
        try:
            # Initialize Pinecone client
            self.client = Pinecone(api_key=self.api_key)
            
            # Create index if it doesn't exist
            if self.index_name not in self.client.list_indexes().names():
                self.client.create_index(
                    name=self.index_name,
                    dimension=1536,  # OpenAI embedding dimension
                    metric="cosine"
                )
                logger.info(f"Created new Pinecone index: {self.index_name}")
            
            # Get index
            self.index = self.client.Index(self.index_name)
            logger.info(f"Connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {str(e)}")
            raise

    def get_index(self):
        """Get the Pinecone index"""
        if not hasattr(self, 'index'):
            self.initialize()
        return self.index

    def get_embedding(self, text: str):
        """Get embedding for text using OpenAI"""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to get embedding: {str(e)}")
            raise

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
                embeddings = self.get_embedding(texts[0])  # Assuming all documents in the batch have the same embedding
                
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
                self.get_index().upsert(vectors=vectors)
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
            query_embedding = self.get_embedding(query)
            
            # Search in Pinecone
            results = self.get_index().query(
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
            self.get_index().delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents from Pinecone")
        except Exception as e:
            logger.error(f"Error deleting documents: {str(e)}")
            raise

    def get_document_count(self) -> int:
        """
        Get the total number of documents in the index.
        """
        try:
            stats = self.get_index().describe_index_stats()
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
            stats = self.get_index().describe_index_stats()
            if stats.total_vector_count == 0:
                logger.info("No vectors in the index to fetch.")
                return None
            
            # Query with a dummy vector to get nearest neighbors, assuming they exist
            dummy_embedding = self.get_embedding("sample query") # Generate a dummy embedding
            results = self.get_index().query(
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