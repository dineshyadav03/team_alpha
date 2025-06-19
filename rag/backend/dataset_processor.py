from document_processor import DocumentProcessor
from vector_store import VectorStore
import os
from typing import List, Dict, Any, Optional
from langchain.schema import Document
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetProcessor:
    def __init__(self, cloud_config: Optional[Dict[str, Any]] = None):
        self.processor = DocumentProcessor(cloud_config)
        self.cloud_config = cloud_config
        self.vector_store = VectorStore()
        self.dataset_path = os.path.join(os.path.dirname(__file__), "dataset")
        
    def initialize(self):
        """Initialize the vector store"""
        self.vector_store.initialize()
        
    def process_dataset(self, dataset_path: str, is_cloud: bool = False, cloud_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Process all documents in a dataset, either local or cloud
        
        Args:
            dataset_path: Path to dataset (local path or cloud path)
            is_cloud: Whether the dataset is in cloud storage
            cloud_type: Type of cloud storage ('aws', 'gcp', 'azure', 'dropbox', 'gdrive')
        """
        processed_docs = []
        
        if is_cloud and cloud_type:
            # Process cloud dataset
            processed_docs.extend(self._process_cloud_dataset(dataset_path, cloud_type))
        else:
            # Process local dataset
            processed_docs.extend(self._process_local_dataset(dataset_path))
            
        return processed_docs

    def _process_local_dataset(self, dataset_path: str) -> List[Dict[str, Any]]:
        """Process all documents in a local dataset directory"""
        processed_docs = []
        
        for root, _, files in os.walk(dataset_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if file.lower().endswith('.pdf'):
                        docs = self.processor.process_pdf(file_path)
                    elif file.lower().endswith(('.txt', '.md')):
                        docs = self.processor.process_text(file_path)
                    else:
                        continue
                        
                    processed_docs.extend(docs)
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
                    
        return processed_docs

    def _process_cloud_dataset(self, dataset_path: str, cloud_type: str) -> List[Dict[str, Any]]:
        """Process all documents in a cloud dataset directory"""
        processed_docs = []
        
        # Get list of files from cloud storage
        if cloud_type == 'aws':
            bucket = self.cloud_config['aws']['bucket']
            s3_client = self.processor.s3_client
            paginator = s3_client.get_paginator('list_objects_v2')
            
            for page in paginator.paginate(Bucket=bucket, Prefix=dataset_path):
                for obj in page.get('Contents', []):
                    file_path = obj['Key']
                    if file_path.lower().endswith(('.pdf', '.txt', '.md')):
                        try:
                            docs = self.processor.process_cloud_document(file_path, cloud_type)
                            processed_docs.extend(docs)
                        except Exception as e:
                            print(f"Error processing {file_path}: {str(e)}")
        
        elif cloud_type == 'gcp':
            bucket = self.processor.gcs_client.bucket(self.cloud_config['gcp']['bucket'])
            blobs = bucket.list_blobs(prefix=dataset_path)
            
            for blob in blobs:
                if blob.name.lower().endswith(('.pdf', '.txt', '.md')):
                    try:
                        docs = self.processor.process_cloud_document(blob.name, cloud_type)
                        processed_docs.extend(docs)
                    except Exception as e:
                        print(f"Error processing {blob.name}: {str(e)}")
        
        elif cloud_type == 'azure':
            container = self.processor.azure_client.get_container_client(
                self.cloud_config['azure']['container']
            )
            blobs = container.list_blobs(name_starts_with=dataset_path)
            
            for blob in blobs:
                if blob.name.lower().endswith(('.pdf', '.txt', '.md')):
                    try:
                        docs = self.processor.process_cloud_document(blob.name, cloud_type)
                        processed_docs.extend(docs)
                    except Exception as e:
                        print(f"Error processing {blob.name}: {str(e)}")
        
        return processed_docs

    def update_dataset(self, dataset_path: str, is_cloud: bool = False, cloud_type: Optional[str] = None):
        """
        Update the dataset by processing new or modified documents
        
        Args:
            dataset_path: Path to dataset (local path or cloud path)
            is_cloud: Whether the dataset is in cloud storage
            cloud_type: Type of cloud storage ('aws', 'gcp', 'azure', 'dropbox', 'gdrive')
        """
        processed_docs = self.process_dataset(dataset_path, is_cloud, cloud_type)
        return processed_docs

if __name__ == "__main__":
    processor = DatasetProcessor()
    processor.initialize()
    processor.process_dataset() 