import os
from pinecone import Pinecone as PineconeClient
from langchain_pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import logging
from langchain.schema import Document
from typing import List
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

        if not all([self.index_name, self.api_key, self.environment]):
            raise ValueError("Missing Pinecone environment variables. Please check your .env file.")

        # Initialize Pinecone connection instance
        self.pinecone_client = PineconeClient(api_key=self.api_key, environment=self.environment)

    def initialize(self):
        logger.info("Initializing vector store...")
        if self.index_name not in self.pinecone_client.list_indexes().names():
            self.pinecone_client.create_index(self.index_name, dimension=1536, metric='cosine')
            logger.info(f"Created new Pinecone index: {self.index_name}")
        self.index = self.pinecone_client.Index(self.index_name)
        logger.info(f"Connected to Pinecone index: {self.index_name}")

    def add_documents(self, documents: List[Document]):
        logger.info(f"Adding {len(documents)} documents to Pinecone...")
        try:
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]

            # Generate embeddings
            vector_embeddings = self.embeddings.embed_documents(texts)

            # Prepare vectors for upsert
            vectors_to_upsert = []
            for i, doc in enumerate(documents):
                metadata = doc.metadata.copy()
                metadata['text'] = doc.page_content

                # Generate a unique ID for each vector. Using UUID is safer than hash().
                unique_id = str(uuid.uuid4())
                
                vector = (
                    unique_id, 
                    vector_embeddings[i],
                    metadata
                )
                vectors_to_upsert.append(vector)
                
                logger.debug(f"Preparing vector: ID={unique_id}, Metadata={metadata.keys()}, EmbeddingShape={len(vector_embeddings[i])}")

            self.index.upsert(vectors=vectors_to_upsert, namespace="")
            logger.info(f"Successfully added {len(vectors_to_upsert)} documents to Pinecone!")
        except Exception as e:
            logger.error(f"Error adding documents to Pinecone: {e}")

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