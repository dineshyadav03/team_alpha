from dataset_processor import DatasetProcessor
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_dataset():
    """Update the dataset with new documents"""
    processor = DatasetProcessor()
    processor.initialize()
    
    # Process only new or modified files
    last_update = get_last_update_time()
    
    # Process new documents
    processor.process_dataset()
    
    # Update last update time
    update_last_update_time()
    
    logger.info("Dataset update completed!")

def get_last_update_time():
    """Get the last update time from the metadata file"""
    metadata_file = os.path.join(os.path.dirname(__file__), "dataset", "processed", "metadata", "last_update.txt")
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            return datetime.fromisoformat(f.read().strip())
    return datetime.min

def update_last_update_time():
    """Update the last update time in the metadata file"""
    metadata_dir = os.path.join(os.path.dirname(__file__), "dataset", "processed", "metadata")
    os.makedirs(metadata_dir, exist_ok=True)
    
    metadata_file = os.path.join(metadata_dir, "last_update.txt")
    with open(metadata_file, 'w') as f:
        f.write(datetime.now().isoformat())

if __name__ == "__main__":
    update_dataset() 