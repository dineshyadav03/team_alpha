'use client'

import { useState, useCallback } from 'react'
import { uploadDocument } from '@/lib/api'

export default function DocumentUpload() {
  const [isUploading, setIsUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<string>('')
  const [isDragging, setIsDragging] = useState(false)

  const handleFileUpload = async (file: File) => {
    if (!file) return

    // Validate file type
    const validTypes = ['.pdf', '.txt']
    const fileExtension = file.name.toLowerCase().slice(file.name.lastIndexOf('.'))
    if (!validTypes.includes(fileExtension)) {
      setUploadStatus('Please upload only PDF or text files')
      return
    }

    setIsUploading(true)
    setUploadStatus('Uploading...')

    try {
      await uploadDocument(file)
      setUploadStatus('Document uploaded successfully!')
    } catch (error) {
      setUploadStatus('Failed to upload document. Please try again.')
      console.error('Upload error:', error)
    } finally {
      setIsUploading(false)
    }
  }

  const onDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(false)
    
    const file = e.dataTransfer.files?.[0]
    if (file) {
      handleFileUpload(file)
    }
  }, [])

  const onDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const onDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  return (
    <div className="p-4 border rounded-lg bg-gray-50">
      <h2 className="text-lg font-semibold mb-2">Upload Documents</h2>
      <p className="text-sm text-gray-600 mb-4">
        Upload PDF or text files for temporary analysis and chat. Documents will be processed but not permanently stored.
      </p>
      
      <div 
        className={`flex items-center gap-4 ${
          isDragging ? 'border-blue-500 bg-blue-50' : ''
        }`}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
      >
        <label className="flex-1">
          <input
            type="file"
            accept=".pdf,.txt"
            onChange={(e) => handleFileUpload(e.target.files?.[0] as File)}
            disabled={isUploading}
            className="hidden"
          />
          <div className={`p-4 border-2 border-dashed rounded-lg text-center cursor-pointer transition-colors
            ${isDragging 
              ? 'border-blue-500 bg-blue-50' 
              : 'border-gray-300 hover:border-blue-500'
            }`}
          >
            {isUploading ? (
              <div className="flex items-center justify-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                <span>Uploading...</span>
              </div>
            ) : (
              <div>
                <p className="mb-2">Drag and drop a file here, or click to select</p>
                <p className="text-sm text-gray-500">Supported formats: PDF, TXT</p>
              </div>
            )}
          </div>
        </label>
      </div>

      {uploadStatus && (
        <p className={`mt-2 text-sm ${
          uploadStatus.includes('success') 
            ? 'text-green-600' 
            : uploadStatus.includes('Please upload') 
              ? 'text-yellow-600'
              : 'text-red-600'
        }`}>
          {uploadStatus}
        </p>
      )}
    </div>
  )
} 