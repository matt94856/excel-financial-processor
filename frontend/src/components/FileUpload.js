import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileSpreadsheet, AlertCircle } from 'lucide-react';
import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from '../config/api';

const FileUpload = ({ onUploadStart, onProcessingStart, onSuccess, onError }) => {
  const [dragActive, setDragActive] = useState(false);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Validate file type
    if (!file.name.match(/\.(xlsx|xls)$/i)) {
      onError('Please upload a valid Excel file (.xlsx or .xls)');
      return;
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      onError('File size must be less than 10MB');
      return;
    }

    try {
      onUploadStart();
      
      const formData = new FormData();
      formData.append('file', file);

      onProcessingStart();

      const response = await axios.post(`${API_BASE_URL}${API_ENDPOINTS.UPLOAD}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000, // 60 second timeout
      });

      onSuccess(response.data);
    } catch (error) {
      console.error('Upload error:', error);
      let errorMessage = 'An error occurred while processing your file.';
      
      if (error.response?.status === 404) {
        errorMessage = 'API endpoint not found. The server may still be deploying. Please try again in a few minutes.';
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.code === 'ECONNABORTED') {
        errorMessage = 'Request timed out. Please try with a smaller file.';
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      onError(errorMessage);
    }
  }, [onUploadStart, onProcessingStart, onSuccess, onError]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls']
    },
    multiple: false,
    onDragEnter: () => setDragActive(true),
    onDragLeave: () => setDragActive(false),
  });

  return (
    <div className="card">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Upload Your Excel File
        </h2>
        <p className="text-gray-600">
          Upload an Excel file to generate professional estimates and financial statements
        </p>
      </div>

      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors duration-200
          ${isDragActive || dragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          }
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center">
          <div className={`
            p-4 rounded-full mb-4 transition-colors duration-200
            ${isDragActive || dragActive
              ? 'bg-primary-100 text-primary-600'
              : 'bg-gray-100 text-gray-600'
            }
          `}>
            {isDragActive || dragActive ? (
              <Upload className="h-8 w-8" />
            ) : (
              <FileSpreadsheet className="h-8 w-8" />
            )}
          </div>
          
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {isDragActive || dragActive
              ? 'Drop your Excel file here'
              : 'Drag & drop your Excel file here'
            }
          </h3>
          
          <p className="text-gray-600 mb-4">
            or click to browse files
          </p>
          
          <div className="text-sm text-gray-500">
            <p>Supported formats: .xlsx, .xls</p>
            <p>Maximum file size: 10MB</p>
          </div>
        </div>
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <div className="flex items-start">
          <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" />
          <div className="text-sm text-blue-800">
            <p className="font-medium mb-1">What happens next?</p>
            <ul className="space-y-1 text-blue-700">
              <li>• Your file will be analyzed for estimates and financial data</li>
              <li>• Data will be formatted with professional styling</li>
              <li>• You'll receive both PDF and Excel versions</li>
              <li>• Processing typically takes 10-30 seconds</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
