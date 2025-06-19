import os
from pinecone_client import PineconeClient
from langchain_pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import logging
from langchain.schema import Document
from typing import List, Dict, Any
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        load_dotenv()
        self.index_name = os.getenv("PINECONE_INDEX")
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.environment = os.getenv("PINECONE_ENVIRONMENT")
        
        logger.info(f"VectorStore Initializing with:")
        logger.info(f"  PINECONE_INDEX: {self.index_name}")
        logger.info(f"  PINECONE_API_KEY: {self.api_key[:5]}...") # Mask for security
        logger.info(f"  PINECONE_ENVIRONMENT: {self.environment}")

        self.embeddings = OpenAIEmbeddings()
        self.client = None
        self.index = None
        self.dimension = 1536  # OpenAI embedding dimension

        if not all([self.index_name, self.api_key, self.environment]):
            raise ValueError("Missing Pinecone environment variables. Please check your .env file.")

    def initialize(self):
        """Initialize Pinecone client and index"""
        try:
            self.client = PineconeClient()
            self.client.initialize()
            self.index = self.client.get_index()
            logger.info("Vector store initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {str(e)}")
            raise

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector store"""
        try:
            if not self.index:
                self.initialize()

            # Prepare vectors for batch upsert
            vectors = []
            for i, doc in enumerate(documents):
                vector = {
                    "id": f"doc_{i}",
                    "values": doc["embedding"],
                    "metadata": {
                        "content": doc["content"],
                        "source": doc["metadata"]["source"]
                    }
                }
                vectors.append(vector)

            # Upsert vectors in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)

            logger.info(f"Successfully added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Failed to add documents to vector store: {str(e)}")
            raise

    def query(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Query the vector store"""
        try:
            if not self.index:
                self.initialize()

            # Get query embedding
            query_embedding = self.client.get_embedding(query)

            # Query the index
            results = self.index.query(
                vector=query_embedding,
                top_k=limit,
                include_metadata=True
            )

            # Format results
            formatted_results = []
            for match in results.matches:
                formatted_results.append({
                    "content": match.metadata["content"],
                    "metadata": {
                        "source": match.metadata["source"]
                    },
                    "score": match.score
                })

            return formatted_results
        except Exception as e:
            logger.error(f"Failed to query vector store: {str(e)}")
            raise

    def similarity_search(self, query, k=4):
        logger.info(f"Searching for documents similar to: {query}")
        try:
            vectorstore = Pinecone(index=self.index, embedding=self.embeddings, text_key="text")
            results = vectorstore.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents.")
            return results
        except Exception as e:
            logger.error(f"Error during similarity search: {e}")
            return []
            
    def delete_all_documents(self):
        logger.info(f"Deleting all documents from Pinecone index: {self.index_name}...")
        try:
            # The delete_all method is part of the Index object
            self.index.delete(delete_all=True)
            logger.info("All documents deleted successfully from Pinecone.")
        except Exception as e:
            logger.error(f"Error deleting all documents from Pinecone: {e}") 