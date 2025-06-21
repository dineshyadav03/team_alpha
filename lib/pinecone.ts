import { Pinecone } from '@pinecone-database/pinecone'
import { OpenAIEmbeddings } from 'langchain/embeddings/openai'
import { Document } from 'langchain/document'
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter'

// Initialize Pinecone client
const pinecone = new Pinecone({
  apiKey: process.env.PINECONE_API_KEY!,
  environment: process.env.PINECONE_ENVIRONMENT!,
})

// Initialize OpenAI embeddings
const embeddings = new OpenAIEmbeddings({
  openAIApiKey: process.env.OPENAI_API_KEY,
})

// Initialize text splitter
const textSplitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,
})

export async function storeDocument(text: string, metadata: any) {
  try {
    // Split text into chunks
    const chunks = await textSplitter.createDocuments([text], [metadata])

    // Generate embeddings for each chunk
    const vectors = await Promise.all(
      chunks.map(async (chunk, index) => {
        const embedding = await embeddings.embedQuery(chunk.pageContent)
        return {
          id: `${metadata.id}-${index}`,
          values: embedding,
          metadata: {
            ...chunk.metadata,
            text: chunk.pageContent,
          },
        }
      })
    )

    // Store vectors in Pinecone
    const index = pinecone.Index(process.env.PINECONE_INDEX_NAME!)
    await index.upsert(vectors)

    return { success: true, chunks: chunks.length }
  } catch (error) {
    console.error('Error storing document:', error)
    throw error
  }
}

export async function searchSimilarDocuments(query: string, k: number = 4) {
  try {
    // Generate embedding for the query
    const queryEmbedding = await embeddings.embedQuery(query)

    // Search in Pinecone
    const index = pinecone.Index(process.env.PINECONE_INDEX_NAME!)
    const results = await index.query({
      vector: queryEmbedding,
      topK: k,
      includeMetadata: true,
    })

    return results.matches.map(match => ({
      text: match.metadata?.text as string,
      score: match.score,
      metadata: match.metadata,
    }))
  } catch (error) {
    console.error('Error searching documents:', error)
    throw error
  }
}

export async function deleteDocument(documentId: string) {
  try {
    const index = pinecone.Index(process.env.PINECONE_INDEX_NAME!)
    await index.deleteMany({
      filter: {
        documentId: documentId,
      },
    })
    return { success: true }
  } catch (error) {
    console.error('Error deleting document:', error)
    throw error
  }
} 