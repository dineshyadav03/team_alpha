# HSA Document RAG Frontend

The frontend application for the HSA Document RAG system, built with Next.js and Tailwind CSS.

## 🛠️ Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Environment Variables
Create a `.env.local` file in the `frontend` directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── api/               # API routes
│   └── page.tsx           # Main page
├── components/            # React components
│   ├── DocumentUpload.tsx # Document upload component
│   └── ChatInterface.tsx  # Chat interface component
├── lib/                   # Utility functions
│   └── api.ts            # API client
└── styles/               # Tailwind CSS styles
```

## 🚀 Usage

### 1. Start the Development Server
```bash
npm run dev
```

### 2. Build for Production
```bash
npm run build
```

### 3. Start Production Server
```bash
npm start
```

## 📱 Features

- **Document Upload**: Upload PDF and text documents
- **Chat Interface**: Ask questions about uploaded documents
- **Smart Search**: Advanced document search using vector embeddings
- **Real-time Responses**: Get instant answers to your queries
- **Modern UI**: Clean and responsive user interface

## 🔧 Configuration

### API Endpoints
- `POST /api/query`: Query documents
- `POST /api/process`: Process new documents

### UI Components
- `DocumentUpload`: Handles document uploads
- `ChatInterface`: Manages chat interactions
- `SearchResults`: Displays search results

## 📝 Notes

- The frontend uses Next.js 14 for the application framework
- Styling is handled by Tailwind CSS
- API communication is managed by the `api.ts` utility
- Real-time updates are handled by client-side state management 