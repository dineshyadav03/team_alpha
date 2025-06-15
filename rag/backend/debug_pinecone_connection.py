import os
import pinecone
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_pinecone_connection():
    logger.info("--- Starting Pinecone Connection Debugger ---")
    load_dotenv() # Load .env file

    api_key = os.getenv("PINECONE_API_KEY")
    environment = os.getenv("PINECONE_ENVIRONMENT")
    index_name = os.getenv("PINECONE_INDEX")
    
    logger.info(f"DEBUG: PINECONE_API_KEY (first 5 chars): {api_key[:5] if api_key else 'None'}...")
    logger.info(f"DEBUG: PINECONE_ENVIRONMENT: {environment}")
    logger.info(f"DEBUG: PINECONE_INDEX: {index_name}")

    if not all([api_key, environment, index_name]):
        logger.error("ERROR: Missing one or more Pinecone environment variables. Please check your .env file.")
        return

    try:
        # Initialize Pinecone
        pc = pinecone.Pinecone(api_key=api_key, environment=environment)
        logger.info("SUCCESS: Pinecone client initialized.")

        # List indexes
        active_indexes = pc.list_indexes().names()
        logger.info(f"SUCCESS: Found active indexes: {active_indexes}")

        # Check if our index exists, create if not
        if index_name not in active_indexes:
            logger.info(f"Index '{index_name}' not found. Attempting to create it...")
            # Make sure dimension and metric match your desired index configuration
            pc.create_index(name=index_name, dimension=1536, metric='cosine')
            logger.info(f"SUCCESS: Index '{index_name}' created.")
        else:
            logger.info(f"Index '{index_name}' already exists.")

        # Connect to the specific index
        index = pc.Index(index_name)
        logger.info(f"SUCCESS: Connected to index '{index_name}'.")

        # --- Test Upsert --- #
        test_vector_id = "debug-test-vector-1"
        test_vector_values = [0.1] * 1536 # A dummy vector of correct dimension
        test_metadata = {"source": "debug_script", "content": "This is a test vector from the debugger.", "text": "This is a test vector from the debugger."}

        logger.info(f"Attempting to upsert test vector: {test_vector_id}...")
        index.upsert(vectors=[(test_vector_id, test_vector_values, test_metadata)], namespace="")
        logger.info("SUCCESS: Test vector upserted.")

        # --- Verify Upsert and Count --- #
        stats = index.describe_index_stats(namespace="")
        total_vectors = stats.namespaces[''].vector_count if '' in stats.namespaces else 0 # Get count from default namespace
        logger.info(f"Index stats - Total vectors in default namespace: {total_vectors}")
        if total_vectors > 0:
            logger.info("SUCCESS: Vectors detected in the index!")
        else:
            logger.warning("WARNING: No vectors detected in the index after upsert.")

        # --- Test Query --- #
        logger.info(f"Attempting to query for test vector: {test_vector_id}...")
        query_results = index.query(vector=test_vector_values, top_k=1, include_metadata=True, namespace="")
        
        if query_results.matches and query_results.matches[0].id == test_vector_id:
            logger.info(f"SUCCESS: Test vector queried back successfully. Score: {query_results.matches[0].score:.4f}")
            logger.info(f"Queried Metadata: {query_results.matches[0].metadata}")
        else:
            logger.error("ERROR: Test vector not found or incorrect in query results.")

    except Exception as e:
        logger.error(f"CRITICAL ERROR during Pinecone connection test: {e}")

    logger.info(f"Attempting to delete test vector: {test_vector_id}...")
    try:
        index.delete(ids=[test_vector_id], namespace="")
        logger.info(f"SUCCESS: Test vector {test_vector_id} deleted.")
    except Exception as e:
        logger.error(f"ERROR: Could not delete test vector: {str(e)}")

    logger.info("--- Pinecone Connection Debugger Finished ---")

if __name__ == "__main__":
    debug_pinecone_connection() 