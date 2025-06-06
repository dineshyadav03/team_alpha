from vector_store import VectorStore
from typing import List, Dict, Any
import json
from datetime import datetime

class DocumentQuerier:
    def __init__(self):
        self.vector_store = VectorStore()
        self.vector_store.initialize()

    def search(self, query: str, filters: Dict[str, Any] = None, k: int = 4) -> List[Dict[str, Any]]:
        """
        Search documents with optional metadata filters
        
        Args:
            query: Search query
            filters: Dictionary of metadata filters (e.g., {"category": "design_documents"})
            k: Number of results to return
        """
        # Get results from vector store
        results = self.vector_store.similarity_search(query, k=k)
        
        # Apply filters if provided
        if filters:
            results = self._filter_results(results, filters)
        
        # Format results
        return self._format_results(results)

    def _filter_results(self, results: List[Any], filters: Dict[str, Any]) -> List[Any]:
        """Filter results based on metadata"""
        filtered_results = []
        for doc in results:
            if all(doc.metadata.get(k) == v for k, v in filters.items()):
                filtered_results.append(doc)
        return filtered_results

    def _format_results(self, results: List[Any]) -> List[Dict[str, Any]]:
        """Format results for output"""
        formatted_results = []
        for doc in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "relevance_score": doc.metadata.get("score", 0)
            })
        return formatted_results

def main():
    querier = DocumentQuerier()
    
    # Example queries
    queries = [
        {
            "query": "What are the key features of the National Cancer Institute?",
            "filters": {"category": "design_documents", "subcategory": "architectural_drawings"}
        },
        {
            "query": "What is the project schedule for NMMC Headquarters?",
            "filters": {"category": "project_management", "subcategory": "project_schedules"}
        },
        {
            "query": "What are the building code requirements for fire safety?",
            "filters": {"category": "regulatory_compliance", "subcategory": "building_codes"}
        }
    ]
    
    for q in queries:
        print(f"\nQuery: {q['query']}")
        print(f"Filters: {q['filters']}")
        results = querier.search(q['query'], q['filters'])
        print("\nResults:")
        for r in results:
            print(f"\nContent: {r['content'][:200]}...")
            print(f"Source: {r['metadata']['source']}")
            print(f"Category: {r['metadata']['category']}")
            print(f"Subcategory: {r['metadata']['subcategory']}")
            print(f"Version: {r['metadata'].get('version', 'N/A')}")
            print(f"Last Updated: {r['metadata'].get('last_updated', 'N/A')}")

if __name__ == "__main__":
    main() 