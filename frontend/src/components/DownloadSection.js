import React from 'react';
import { Download, FileText, FileSpreadsheet, CheckCircle, RotateCcw } from 'lucide-react';
import { API_BASE_URL } from '../config/api';

const DownloadSection = ({ downloadData, onReset }) => {
  const handleDownload = (url, filename) => {
    const link = document.createElement('a');
    link.href = `${API_BASE_URL}${url}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      {/* Success Message */}
      <div className="card">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-success-100 rounded-full mb-4">
            <CheckCircle className="h-8 w-8 text-success-600" />
          </div>
          
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Processing Complete!
          </h2>
          
          <p className="text-gray-600 mb-6">
            Your Excel file has been successfully processed. Download your professional documents below.
          </p>
          
          <div className="text-sm text-gray-500">
            <p><strong>Original file:</strong> {downloadData.original_filename}</p>
            <p><strong>File ID:</strong> {downloadData.file_id}</p>
          </div>
        </div>
      </div>

      {/* Download Options */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* PDF Download */}
        <div className="card">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-red-100 rounded-lg mb-4">
              <FileText className="h-6 w-6 text-red-600" />
            </div>
            
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              PDF Document
            </h3>
            
            <p className="text-gray-600 mb-4">
              Professional PDF with formatted estimates and financial statements
            </p>
            
            <button
              onClick={() => handleDownload(downloadData.pdf_download, `${downloadData.original_filename}_processed.pdf`)}
              className="btn-primary w-full flex items-center justify-center"
            >
              <Download className="h-4 w-4 mr-2" />
              Download PDF
            </button>
          </div>
        </div>

        {/* Excel Download */}
        <div className="card">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg mb-4">
              <FileSpreadsheet className="h-6 w-6 text-green-600" />
            </div>
            
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Excel Document
            </h3>
            
            <p className="text-gray-600 mb-4">
              Clean, formatted Excel file with professional styling
            </p>
            
            <button
              onClick={() => handleDownload(downloadData.excel_download, `${downloadData.original_filename}_processed.xlsx`)}
              className="btn-success w-full flex items-center justify-center"
            >
              <Download className="h-4 w-4 mr-2" />
              Download Excel
            </button>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="card">
        <div className="text-center">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            What would you like to do next?
          </h3>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={onReset}
              className="btn-secondary flex items-center justify-center"
            >
              <RotateCcw className="h-4 w-4 mr-2" />
              Process Another File
            </button>
            
            <button
              onClick={() => window.print()}
              className="btn-secondary flex items-center justify-center"
            >
              <FileText className="h-4 w-4 mr-2" />
              Print This Page
            </button>
          </div>
        </div>
      </div>

      {/* Features Reminder */}
      <div className="card bg-blue-50 border-blue-200">
        <div className="text-center">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">
            Your documents include:
          </h3>
          
          <div className="grid md:grid-cols-2 gap-4 text-sm text-blue-800">
            <div>
              <ul className="space-y-1">
                <li>• Professional formatting and styling</li>
                <li>• Automatic calculations and totals</li>
                <li>• Clean table borders and alignment</li>
              </ul>
            </div>
            <div>
              <ul className="space-y-1">
                <li>• Currency formatting</li>
                <li>• Summary sections</li>
                <li>• Client-ready presentation</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DownloadSection;
