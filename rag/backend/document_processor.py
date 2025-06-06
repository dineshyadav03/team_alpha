from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
from langchain.schema import Document
import json
import os
from datetime import datetime

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

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