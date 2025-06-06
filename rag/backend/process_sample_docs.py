from dataset_processor import DatasetProcessor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Process the sample documents and add them to Pinecone"""
    logger.info("Starting to process sample documents...")
    
    # Initialize the processor
    processor = DatasetProcessor()
    processor.initialize()
    
    # Process the dataset
    processor.process_dataset()
    
    logger.info("Sample documents processed and added to Pinecone!")

if __name__ == "__main__":
    main() 