import os
from document_processor import DocumentProcessor
from dataset_processor import DatasetProcessor
from vector_store import VectorStore
from pinecone_client import PineconeClient
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_pinecone_connection():
    """Test Pinecone connection and index"""
    logger.info("Testing Pinecone connection...")
    try:
        client = PineconeClient()
        client.initialize()
        logger.info("✅ Pinecone connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Pinecone connection failed: {str(e)}")
        return False

def test_document_processing():
    """Test document processing with sample files"""
    logger.info("Testing document processing...")
    try:
        processor = DocumentProcessor()
        
        # Test PDF processing
        pdf_path = "dataset/design_documents/sample.pdf"
        if os.path.exists(pdf_path):
            docs = processor.process_pdf(pdf_path)
            logger.info(f"✅ PDF processing successful: {len(docs)} chunks created")
        else:
            logger.warning("⚠️ Sample PDF not found, skipping PDF test")
        
        # Test text processing
        txt_path = "dataset/regulatory_compliance/sample.txt"
        if os.path.exists(txt_path):
            docs = processor.process_text(txt_path)
            logger.info(f"✅ Text processing successful: {len(docs)} chunks created")
        else:
            logger.warning("⚠️ Sample text file not found, skipping text test")
            
        return True
    except Exception as e:
        logger.error(f"❌ Document processing failed: {str(e)}")
        return False

def test_vector_store():
    """Test vector storage and retrieval"""
    logger.info("Testing vector store...")
    try:
        vector_store = VectorStore()
        vector_store.initialize()
        
        # Test adding documents
        test_docs = [
            {"content": "Test document 1", "metadata": {"source": "test1"}},
            {"content": "Test document 2", "metadata": {"source": "test2"}}
        ]
        vector_store.add_documents(test_docs)
        logger.info("✅ Document addition successful")
        
        # Test querying
        results = vector_store.query("test document", limit=2)
        logger.info(f"✅ Query successful: {len(results)} results found")
        
        return True
    except Exception as e:
        logger.error(f"❌ Vector store test failed: {str(e)}")
        return False

def test_dataset_processor():
    """Test dataset processing"""
    logger.info("Testing dataset processor...")
    try:
        processor = DatasetProcessor()
        
        # Test local dataset processing
        docs = processor.process_dataset("dataset")
        logger.info(f"✅ Dataset processing successful: {len(docs)} documents processed")
        
        return True
    except Exception as e:
        logger.error(f"❌ Dataset processing failed: {str(e)}")
        return False

def test_cloud_integration():
    """Test cloud storage integration"""
    logger.info("Testing cloud integration...")
    try:
        # Test AWS S3
        cloud_config = {
            'aws': {
                'access_key': os.getenv('AWS_ACCESS_KEY'),
                'secret_key': os.getenv('AWS_SECRET_KEY'),
                'region': os.getenv('AWS_REGION'),
                'bucket': os.getenv('AWS_BUCKET')
            }
        }
        
        processor = DatasetProcessor(cloud_config)
        docs = processor.process_dataset("test/", is_cloud=True, cloud_type='aws')
        logger.info(f"✅ Cloud integration successful: {len(docs)} documents processed")
        
        return True
    except Exception as e:
        logger.error(f"❌ Cloud integration failed: {str(e)}")
        return False

def run_all_tests():
    """Run all system tests"""
    logger.info("Starting system tests...")
    
    tests = [
        ("Pinecone Connection", test_pinecone_connection),
        ("Document Processing", test_document_processing),
        ("Vector Store", test_vector_store),
        ("Dataset Processor", test_dataset_processor),
        ("Cloud Integration", test_cloud_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\nRunning {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} failed with error: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    logger.info("\n=== Test Summary ===")
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")

if __name__ == "__main__":
    load_dotenv()  # Load environment variables
    run_all_tests() 