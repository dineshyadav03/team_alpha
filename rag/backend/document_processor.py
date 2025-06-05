from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def process_pdf(self, file_path: str) -> List[Document]:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        return self._split_documents(docs)

    def process_text(self, file_path: str) -> List[Document]:
        loader = TextLoader(file_path)
        docs = loader.load()
        return self._split_documents(docs)

    def _split_documents(self, docs: List[Document]) -> List[Document]:
        split_docs = self.text_splitter.split_documents(docs)
        return [
            Document(
                page_content=doc.page_content,
                metadata={
                    **doc.metadata,
                    "source": doc.metadata.get("source", ""),
                    "page": doc.metadata.get("page", 0)
                }
            )
            for doc in split_docs
        ] 