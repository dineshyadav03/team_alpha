import os
from dotenv import load_dotenv
import pinecone
from langchain.embeddings import OpenAIEmbeddings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_pinecone_setup():
    """Test Pinecone connection and index setup"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get environment variables
        api_key = os.getenv("PINECONE_API_KEY")
        environment = os.getenv("PINECONE_ENVIRONMENT")
        index_name = os.getenv("PINECONE_INDEX")
        
        if not all([api_key, environment, index_name]):
            logger.error("Missing environment variables. Please check your .env file.")
            return False
        
        # Initialize Pinecone
        logger.info("Initializing Pinecone...")
        pinecone.init(api_key=api_key, environment=environment)
        
        # Check if index exists
        if index_name not in pinecone.list_indexes():
            logger.error(f"Index '{index_name}' not found. Please create it in Pinecone console.")
            return False
        
        # Get index
        index = pinecone.Index(index_name)
        
        # Test embedding
        logger.info("Testing embedding generation...")
        embeddings = OpenAIEmbeddings()
        test_text = "This is a test document for HSA."
        test_embedding = embeddings.embed_query(test_text)
        
        # Test vector upsert
        logger.info("Testing vector upsert...")
        index.upsert(vectors=[("test-1", test_embedding)])
        
        # Test vector query
        logger.info("Testing vector query...")
        results = index.query(vector=test_embedding, top_k=1)
        
        logger.info("All tests passed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error during Pinecone setup test: {str(e)}")
        return False

if __name__ == "__main__":
    test_pinecone_setup() 