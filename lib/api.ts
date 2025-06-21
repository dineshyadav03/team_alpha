const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '';

export interface SearchResult {
  content: string;
  metadata: {
    source: string;
    page?: number;
  };
  score: number;
}

export async function uploadDocument(file: File): Promise<void> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('/api/upload', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to upload document');
  }
}

export async function searchDocuments(query: string): Promise<SearchResult[]> {
  const response = await fetch(`${API_BASE_URL}/api/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error('Failed to search documents');
  }

  return response.json();
} 