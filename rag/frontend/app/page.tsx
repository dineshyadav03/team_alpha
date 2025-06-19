'use client'

import { useState } from 'react'
import { useChat, Message } from 'ai/react'
import { searchDocuments } from '@/lib/api'
import DocumentUpload from '@/components/DocumentUpload'

export default function Chat() {
  const [isLoading, setIsLoading] = useState(false)
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat',
    onResponse: (response: Response) => {
      setIsLoading(false)
    },
  })

  const handleSearch = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!input.trim()) return

    setIsLoading(true)
    try {
      const results = await searchDocuments(input)
      // Here we'll handle the search results
      console.log('Search results:', results)
    } catch (error) {
      console.error('Search error:', error)
    }
    setIsLoading(false)
  }

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold">HSA Information Assistant</h1>
        <p className="text-gray-600">Ask questions about HSA and Maharashtra</p>
      </div>

      {/* Document Upload */}
      <div className="mb-8">
        <DocumentUpload />
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto mb-4 space-y-4">
        {messages.map((message: Message) => (
          <div
            key={message.id}
            className={`p-4 rounded-lg ${
              message.role === 'assistant'
                ? 'bg-blue-100 ml-4'
                : 'bg-gray-100 mr-4'
            }`}
          >
            <p className="text-sm font-semibold mb-1">
              {message.role === 'assistant' ? 'Assistant' : 'You'}
            </p>
            <p>{message.content}</p>
          </div>
        ))}
        {isLoading && (
          <div className="p-4 rounded-lg bg-blue-100 ml-4">
            <p className="text-sm font-semibold mb-1">Assistant</p>
            <p>Thinking...</p>
          </div>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Ask a question about HSA or Maharashtra..."
          className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-blue-300"
        >
          {isLoading ? 'Thinking...' : 'Ask'}
        </button>
      </form>
    </div>
  )
} 