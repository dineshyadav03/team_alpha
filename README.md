# HSA Information Assistant

A modern AI-powered chat application for Housing Society Association (HSA) and Maharashtra regulations, built with Next.js, OpenAI, and Pinecone.

## Features

- 📝 Document Upload: Upload PDF and text documents about HSA and Maharashtra regulations
- 💬 AI Chat Interface: Ask questions about uploaded documents
- 🔍 Smart Search: Advanced document search using vector embeddings
- 🚀 Real-time Responses: Get instant answers to your queries
- 📱 Modern UI: Clean and responsive user interface

## Tech Stack

- **Frontend**: Next.js 14, React, TypeScript, TailwindCSS
- **AI/ML**: OpenAI GPT-3.5, OpenAI Embeddings
- **Vector Database**: Pinecone
- **Document Processing**: PDF-Parse, LangChain

## Prerequisites

- Node.js 18+ and npm
- OpenAI API key
- Pinecone account and API key

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hsa-chat
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env.local` file in the root directory with the following variables:
   ```
   # OpenAI API Key
   OPENAI_API_KEY=your-openai-api-key

   # Pinecone Configuration
   PINECONE_API_KEY=your-pinecone-api-key
   PINECONE_ENVIRONMENT=your-pinecone-environment
   PINECONE_INDEX_NAME=your-index-name

   # API Configuration
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Set up Pinecone**
   - Create a Pinecone account at https://www.pinecone.io
   - Create a new index with dimension 1536 (for OpenAI embeddings)
   - Copy your API key and environment details

5. **Run the development server**
   ```bash
   npm run dev
   ```

## Usage

1. **Upload Documents**
   - Click the upload area or drag and drop files
   - Supported formats: PDF, TXT
   - Documents are automatically processed and stored in Pinecone

2. **Ask Questions**
   - Type your question in the chat interface
   - The AI will search through uploaded documents
   - Get instant, relevant answers based on document content

3. **Example Questions**
   - "What are the maintenance charges?"
   - "How to file a complaint?"
   - "What are the parking rules?"
   - "How to apply for membership?"

## Project Structure

```
├── app/                    # Next.js app directory
│   ├── api/               # API routes
│   │   ├── chat/         # Chat endpoint
│   │   └── upload/       # Document upload endpoint
│   └── page.tsx          # Main page
├── components/            # React components
│   └── DocumentUpload.tsx # Document upload component
├── lib/                   # Utility functions
│   ├── api.ts            # API client
│   └── pinecone.ts       # Pinecone integration
└── public/               # Static assets
```

## How It Works

1. **Document Processing**
   - Documents are split into chunks
   - Each chunk is converted to embeddings
   - Embeddings are stored in Pinecone

2. **Question Answering**
   - User question is converted to embedding
   - Similar document chunks are retrieved
   - AI generates answer using retrieved context

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
