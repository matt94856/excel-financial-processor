import React from 'react';
import { Loader2, FileSpreadsheet, CheckCircle } from 'lucide-react';

const ProcessingStatus = ({ status }) => {
  const isUploading = status === 'uploading';
  const isProcessing = status === 'processing';

  return (
    <div className="card">
      <div className="text-center">
        <div className="mb-6">
          {isUploading ? (
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
              <FileSpreadsheet className="h-8 w-8 text-blue-600" />
            </div>
          ) : (
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
              <Loader2 className="h-8 w-8 text-primary-600 animate-spin" />
            </div>
          )}
        </div>

        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          {isUploading ? 'Uploading File...' : 'Processing Your Data...'}
        </h2>

        <p className="text-gray-600 mb-6">
          {isUploading
            ? 'Please wait while we upload your Excel file to our secure server.'
            : 'We\'re analyzing your data and generating professional documents. This may take a few moments.'
          }
        </p>

        {/* Progress Steps */}
        <div className="max-w-md mx-auto">
          <div className="flex items-center justify-between mb-4">
            <div className={`flex items-center ${isUploading ? 'text-primary-600' : 'text-gray-400'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                isUploading ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-600'
              }`}>
                {isUploading ? <CheckCircle className="h-4 w-4" /> : '1'}
              </div>
              <span className="ml-2 text-sm font-medium">Upload</span>
            </div>
            
            <div className={`flex-1 h-0.5 mx-4 ${
              isProcessing ? 'bg-primary-600' : 'bg-gray-200'
            }`}></div>
            
            <div className={`flex items-center ${isProcessing ? 'text-primary-600' : 'text-gray-400'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                isProcessing ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-600'
              }`}>
                {isProcessing ? <Loader2 className="h-4 w-4 animate-spin" /> : '2'}
              </div>
              <span className="ml-2 text-sm font-medium">Process</span>
            </div>
            
            <div className="flex-1 h-0.5 mx-4 bg-gray-200"></div>
            
            <div className="flex items-center text-gray-400">
              <div className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium bg-gray-200 text-gray-600">
                3
              </div>
              <span className="ml-2 text-sm font-medium">Complete</span>
            </div>
          </div>
        </div>

        {/* Processing Details */}
        {isProcessing && (
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-900 mb-2">Processing Steps:</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Analyzing Excel structure and content</li>
              <li>• Identifying estimates and financial statements</li>
              <li>• Applying professional formatting</li>
              <li>• Generating PDF and Excel outputs</li>
            </ul>
          </div>
        )}

        <div className="mt-6 text-sm text-gray-500">
          <p>This process is secure and your data is processed locally on our servers.</p>
        </div>
      </div>
    </div>
  );
};

export default ProcessingStatus;
