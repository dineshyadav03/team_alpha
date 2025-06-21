import { OpenAIStream } from 'ai/streams'
import { StreamingTextResponse } from 'ai/server'
import { Configuration, OpenAIApi } from 'openai-edge'
import { searchSimilarDocuments } from '@/lib/pinecone'

// Create an OpenAI API client
const config = new Configuration({
  apiKey: process.env.OPENAI_API_KEY
})
const openai = new OpenAIApi(config)

export const runtime = 'edge'

export async function POST(req: Request) {
  try {
    const { messages } = await req.json()
    const lastMessage = messages[messages.length - 1]

    // Search for relevant documents
    const relevantDocs = await searchSimilarDocuments(lastMessage.content)

    // Create the system message with context
    const systemMessage = {
      role: 'system',
      content: `You are a conversational AI assistant for HSA (Hiten Sethi & Associates). You can chat naturally about any topic while also providing specific information from documents when relevant.
      
      When relevant document context is available, use it to provide detailed, accurate answers. When no relevant documents are found, engage in natural conversation and provide helpful general information.
      
      Context from documents:
      ${relevantDocs.map(doc => doc.text).join('\n\n')}`
    }

    // Create the chat completion
    const response = await openai.createChatCompletion({
      model: 'gpt-3.5-turbo',
      stream: true,
      messages: [systemMessage, ...messages],
      temperature: 0.7,
      max_tokens: 500,
    })

    // Convert the response into a friendly text-stream
    const stream = OpenAIStream(response)
    return new StreamingTextResponse(stream)
  } catch (error) {
    console.error('Error in chat route:', error)
    return new Response(
      JSON.stringify({ error: 'Internal server error' }),
      { status: 500 }
    )
  }
} 