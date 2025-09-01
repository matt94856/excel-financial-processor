import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ProcessingStatus from './components/ProcessingStatus';
import DownloadSection from './components/DownloadSection';
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  const [uploadStatus, setUploadStatus] = useState('idle'); // 'idle', 'uploading', 'processing', 'completed', 'error'
  const [downloadData, setDownloadData] = useState(null);
  const [error, setError] = useState(null);

  const handleUploadSuccess = (data) => {
    setUploadStatus('completed');
    setDownloadData(data);
    setError(null);
  };

  const handleUploadError = (errorMessage) => {
    setUploadStatus('error');
    setError(errorMessage);
    setDownloadData(null);
  };

  const handleReset = () => {
    setUploadStatus('idle');
    setDownloadData(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Excel Financial Processor
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Transform your Excel data into professional estimates and financial statements
            </p>
          </div>

          {/* Main Content */}
          <div className="space-y-8">
            {uploadStatus === 'idle' && (
              <FileUpload
                onUploadStart={() => setUploadStatus('uploading')}
                onProcessingStart={() => setUploadStatus('processing')}
                onSuccess={handleUploadSuccess}
                onError={handleUploadError}
              />
            )}

            {(uploadStatus === 'uploading' || uploadStatus === 'processing') && (
              <ProcessingStatus status={uploadStatus} />
            )}

            {uploadStatus === 'completed' && downloadData && (
              <DownloadSection
                downloadData={downloadData}
                onReset={handleReset}
              />
            )}

            {uploadStatus === 'error' && (
              <div className="card">
                <div className="text-center">
                  <div className="text-red-600 text-6xl mb-4">⚠️</div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">
                    Processing Error
                  </h2>
                  <p className="text-gray-600 mb-6">
                    {error || 'An error occurred while processing your file. Please try again.'}
                  </p>
                  <button
                    onClick={handleReset}
                    className="btn-primary"
                  >
                    Try Again
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Features Section */}
          <div className="mt-16 grid md:grid-cols-3 gap-8">
            <div className="card text-center">
              <div className="text-primary-600 text-4xl mb-4">📊</div>
              <h3 className="text-xl font-semibold mb-2">Smart Processing</h3>
              <p className="text-gray-600">
                Automatically detects estimates and financial statements in your Excel files
              </p>
            </div>
            
            <div className="card text-center">
              <div className="text-primary-600 text-4xl mb-4">🎨</div>
              <h3 className="text-xl font-semibold mb-2">Professional Formatting</h3>
              <p className="text-gray-600">
                Generates clean, client-ready documents with proper formatting and styling
              </p>
            </div>
            
            <div className="card text-center">
              <div className="text-primary-600 text-4xl mb-4">📄</div>
              <h3 className="text-xl font-semibold mb-2">Multiple Formats</h3>
              <p className="text-gray-600">
                Download your processed data as both PDF and Excel files
              </p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
