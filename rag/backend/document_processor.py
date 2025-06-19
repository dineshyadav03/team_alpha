from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict, Any, Optional
from langchain.schema import Document
import json
import os
from datetime import datetime
import boto3
from google.cloud import storage
from azure.storage.blob import BlobServiceClient
import tempfile
import requests

class DocumentProcessor:
    def __init__(self, cloud_config: Optional[Dict[str, Any]] = None):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.cloud_config = cloud_config or {}
        self._init_cloud_clients()

    def _init_cloud_clients(self):
        """Initialize cloud storage clients based on configuration"""
        if 'aws' in self.cloud_config:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.cloud_config['aws']['access_key'],
                aws_secret_access_key=self.cloud_config['aws']['secret_key'],
                region_name=self.cloud_config['aws']['region']
            )
        
        if 'gcp' in self.cloud_config:
            self.gcs_client = storage.Client.from_service_account_json(
                self.cloud_config['gcp']['credentials_file']
            )
        
        if 'azure' in self.cloud_config:
            self.azure_client = BlobServiceClient.from_connection_string(
                self.cloud_config['azure']['connection_string']
            )

    def process_cloud_document(self, cloud_path: str, cloud_type: str) -> List[Document]:
        """Process a document from cloud storage"""
        # Download file to temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            self._download_from_cloud(cloud_path, temp_path, cloud_type)
            
            # Process based on file type
            if cloud_path.lower().endswith('.pdf'):
                return self.process_pdf(temp_path)
            else:
                return self.process_text(temp_path)

    def _download_from_cloud(self, cloud_path: str, local_path: str, cloud_type: str):
        """Download file from cloud storage"""
        if cloud_type == 'aws':
            bucket = self.cloud_config['aws']['bucket']
            self.s3_client.download_file(bucket, cloud_path, local_path)
        
        elif cloud_type == 'gcp':
            bucket = self.gcs_client.bucket(self.cloud_config['gcp']['bucket'])
            blob = bucket.blob(cloud_path)
            blob.download_to_filename(local_path)
        
        elif cloud_type == 'azure':
            container = self.azure_client.get_container_client(
                self.cloud_config['azure']['container']
            )
            blob = container.get_blob_client(cloud_path)
            with open(local_path, "wb") as file:
                file.write(blob.download_blob().readall())
        
        elif cloud_type == 'dropbox':
            headers = {
                'Authorization': f"Bearer {self.cloud_config['dropbox']['access_token']}"
            }
            response = requests.get(
                f"https://content.dropboxapi.com/2/files/download",
                headers=headers,
                json={"path": cloud_path}
            )
            with open(local_path, 'wb') as f:
                f.write(response.content)
        
        elif cloud_type == 'gdrive':
            # Google Drive API implementation
            pass

    def process_pdf(self, file_path: str) -> List[Document]:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        return self._process_documents(docs, file_path, "pdf")

    def process_text(self, file_path: str) -> List[Document]:
        loader = TextLoader(file_path)
        docs = loader.load()
        return self._process_documents(docs, file_path, "text")

    def _process_documents(self, docs: List[Document], file_path: str, file_type: str) -> List[Document]:
        # Extract metadata from file content
        metadata = self._extract_metadata(docs[0].page_content)
        
        # Add file-specific metadata
        metadata.update({
            "source": file_path,
            "file_type": file_type,
            "processing_date": datetime.now().isoformat(),
            "category": self._get_category_from_path(file_path),
            "subcategory": self._get_subcategory_from_path(file_path)
        })

        # Split documents
        split_docs = self.text_splitter.split_documents(docs)
        
        # Add metadata to each chunk
        return [
            Document(
                page_content=doc.page_content,
                metadata={
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(split_docs)
                }
            )
            for i, doc in enumerate(split_docs)
        ]

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from document content"""
        try:
            # Look for metadata section
            if "Metadata:" in content:
                metadata_str = content.split("Metadata:")[1].strip()
                return json.loads(metadata_str)
        except:
            pass
        return {}

    def _get_category_from_path(self, file_path: str) -> str:
        """Extract category from file path"""
        parts = file_path.split(os.sep)
        if "design_documents" in parts:
            return "design_documents"
        elif "regulatory_compliance" in parts:
            return "regulatory_compliance"
        elif "project_management" in parts:
            return "project_management"
        elif "construction_documents" in parts:
            return "construction_documents"
        elif "marketing_materials" in parts:
            return "marketing_materials"
        return "other"

    def _get_subcategory_from_path(self, file_path: str) -> str:
        """Extract subcategory from file path"""
        parts = file_path.split(os.sep)
        for part in parts:
            if part in ["architectural_drawings", "interior_designs", "landscape_plans", "urban_designs",
                       "statutory_approvals", "building_codes", "green_certifications",
                       "project_schedules", "budget_reports", "stakeholder_communications",
                       "tender_documents", "construction_drawings", "quality_control",
                       "project_portfolios", "award_submissions", "promotional_materials"]:
                return part
        return "other" 