from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from typing import List
import pinecone
import os

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.index = None

    def initialize(self):
        pinecone.init(
            api_key=os.getenv("PINECONE_API_KEY"),
            environment=os.getenv("PINECONE_ENVIRONMENT")
        )
        self.index = pinecone.Index(os.getenv("PINECONE_INDEX"))

    def add_documents(self, documents: List[Document]):
        vectorstore = Pinecone.from_documents(
            documents=documents,
            embedding=self.embeddings,
            index_name=os.getenv("PINECONE_INDEX")
        )
        return vectorstore

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        vectorstore = Pinecone.from_existing_index(
            index_name=os.getenv("PINECONE_INDEX"),
            embedding=self.embeddings
        )
        return vectorstore.similarity_search(query, k=k) 