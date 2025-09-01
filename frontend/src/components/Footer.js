import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white mt-16">
      <div className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">Excel Financial Processor</h3>
            <p className="text-gray-300 text-sm">
              Transform your Excel data into professional estimates and financial statements 
              with our intelligent processing system.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Features</h3>
            <ul className="text-gray-300 text-sm space-y-2">
              <li>• Smart Excel parsing</li>
              <li>• Professional formatting</li>
              <li>• PDF & Excel export</li>
              <li>• Automatic calculations</li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Support</h3>
            <p className="text-gray-300 text-sm">
              For support or questions, please contact our team. 
              We're here to help you create professional financial documents.
            </p>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-8 text-center">
          <p className="text-gray-400 text-sm">
            © 2024 Excel Financial Processor. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
