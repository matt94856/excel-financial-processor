import React from 'react';
import { FileSpreadsheet, Calculator } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-primary-600 p-2 rounded-lg">
              <FileSpreadsheet className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Excel Financial Processor
              </h1>
              <p className="text-sm text-gray-600">
                Professional Document Generation
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <Calculator className="h-4 w-4" />
            <span>Powered by AI Processing</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
