import os
import yaml
from typing import List, Dict, Any
from pypdf import PdfReader
from PIL import Image
import pytesseract
from pathlib import Path

class DocumentProcessor:
    def __init__(self, config_path: str = "../config.yaml"):
        """Initialize the document processor with configuration."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.chunk_size = self.config['chunk_size']
        self.chunk_overlap = self.config['chunk_overlap']
        self.metadata_fields = self.config['metadata_fields']
        self.document_types = self.config['document_types']
        self.scope = self.config['scope']

    def process_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Process a PDF file and return chunks with metadata."""
        chunks = []
        reader = PdfReader(file_path)
        
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            page_chunks = self._chunk_text(text)
            
            for chunk in page_chunks:
                chunks.append({
                    'content': chunk,
                    'metadata': {
                        'state': self.scope['state'],
                        'firm': self.scope['firm'],
                        'document_type': self._infer_document_type(file_path),
                        'page_number': page_num + 1,
                        'source_file': os.path.basename(file_path)
                    }
                })
        
        return chunks

    def process_image(self, file_path: str) -> List[Dict[str, Any]]:
        """Process an image file using OCR and return chunks with metadata."""
        chunks = []
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        
        page_chunks = self._chunk_text(text)
        for chunk in page_chunks:
            chunks.append({
                'content': chunk,
                'metadata': {
                    'state': self.scope['state'],
                    'firm': self.scope['firm'],
                    'document_type': self._infer_document_type(file_path),
                    'page_number': 1,
                    'source_file': os.path.basename(file_path)
                }
            })
        
        return chunks

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - self.chunk_overlap

        return chunks

    def _infer_document_type(self, file_path: str) -> str:
        """Infer document type from filename and content."""
        filename = os.path.basename(file_path).lower()
        
        for doc_type in self.document_types:
            if doc_type in filename:
                return doc_type
        
        # Default to first document type if can't infer
        return self.document_types[0]

    def process_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Process all supported files in a directory."""
        all_chunks = []
        supported_extensions = {'.pdf', '.png', '.jpg', '.jpeg'}
        
        for file_path in Path(directory_path).rglob('*'):
            if file_path.suffix.lower() in supported_extensions:
                try:
                    if file_path.suffix.lower() == '.pdf':
                        chunks = self.process_pdf(str(file_path))
                    else:
                        chunks = self.process_image(str(file_path))
                    all_chunks.extend(chunks)
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
        
        return all_chunks

if __name__ == "__main__":
    # Example usage
    processor = DocumentProcessor()
    chunks = processor.process_directory("../data")
    print(f"Processed {len(chunks)} chunks from documents") 