const XLSX = require('xlsx');
const { jsPDF } = require('jspdf');
require('jspdf-autotable');

exports.handler = async (event, context) => {
  // Handle CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'POST, OPTIONS, GET'
  };

  // Log the request for debugging
  console.log('Upload function called with method:', event.httpMethod);

  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: headers,
      body: ''
    };
  }

  try {
    // Parse multipart form data
    const boundary = event.headers['content-type']?.split('boundary=')[1];
    if (!boundary) {
      throw new Error('No boundary found in content-type header');
    }

    const body = Buffer.from(event.body, 'base64');
    const parts = body.toString().split(`--${boundary}`);
    
    let fileData = null;
    let filename = 'sample.xlsx';
    
    // Extract file data from multipart form
    for (const part of parts) {
      if (part.includes('Content-Disposition: form-data') && part.includes('filename=')) {
        const filenameMatch = part.match(/filename="([^"]+)"/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
        
        const fileStart = part.indexOf('\r\n\r\n') + 4;
        const fileEnd = part.lastIndexOf('\r\n');
        if (fileStart > 3 && fileEnd > fileStart) {
          fileData = part.substring(fileStart, fileEnd);
          break;
        }
      }
    }

    if (!fileData) {
      throw new Error('No file data found in request');
    }

    // Process Excel file
    const workbook = XLSX.read(fileData, { type: 'base64' });
    const processedData = processExcelData(workbook, filename);
    
    const fileId = Math.random().toString(36).substr(2, 9);
    
    // Store processed data (in a real app, you'd store this in a database)
    // For now, we'll generate the files immediately
    
    const response = {
      file_id: fileId,
      original_filename: filename,
      pdf_download: `/api/download/${fileId}_processed.pdf`,
      excel_download: `/api/download/${fileId}_processed.xlsx`,
      status: 'success',
      message: 'File processed successfully',
      data: processedData
    };
    
    console.log('Returning response:', response);
    
    return {
      statusCode: 200,
      headers: headers,
      body: JSON.stringify(response)
    };
    
  } catch (error) {
    const errorResponse = {
      error: `Error processing file: ${error.message}`
    };
    console.log('Error occurred:', errorResponse);
    
    return {
      statusCode: 500,
      headers: headers,
      body: JSON.stringify(errorResponse)
    };
  }
};

function processExcelData(workbook, filename) {
  const result = {
    estimates: [],
    financial_statements: [],
    sheets: {},
    summary: {
      total_estimates: 0,
      total_financial_statements: 0,
      total_sheets: 0,
      grand_total: 0
    }
  };

  // Process each sheet
  workbook.SheetNames.forEach(sheetName => {
    const worksheet = workbook.Sheets[sheetName];
    const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
    
    result.sheets[sheetName] = {
      title: sheetName,
      headers: data[0] || [],
      data: data.slice(1).map(row => {
        const obj = {};
        data[0]?.forEach((header, index) => {
          obj[header] = row[index];
        });
        return obj;
      })
    };

    // Detect if this is an estimate or financial statement
    const sheetText = JSON.stringify(data).toLowerCase();
    
    if (sheetText.includes('estimate') || sheetText.includes('project') || sheetText.includes('hours') || sheetText.includes('rate')) {
      // Process as estimate
      const estimate = processEstimate(data, sheetName);
      result.estimates.push(estimate);
      result.summary.total_estimates++;
      result.summary.grand_total += estimate.total || 0;
    } else if (sheetText.includes('income') || sheetText.includes('balance') || sheetText.includes('revenue') || sheetText.includes('expense')) {
      // Process as financial statement
      const financial = processFinancialStatement(data, sheetName);
      result.financial_statements.push(financial);
      result.summary.total_financial_statements++;
    }
  });

  result.summary.total_sheets = workbook.SheetNames.length;
  return result;
}

function processEstimate(data, sheetName) {
  const headers = data[0] || [];
  const rows = data.slice(1);
  
  const items = rows.map(row => {
    const item = {};
    headers.forEach((header, index) => {
      item[header] = row[index];
    });
    
    // Calculate total if we have quantity and rate
    if (item.Quantity && item.Rate) {
      item.Total = parseFloat(item.Quantity) * parseFloat(item.Rate);
    } else if (item.Hours && item.Rate) {
      item.Total = parseFloat(item.Hours) * parseFloat(item.Rate);
    }
    
    return item;
  });

  const total = items.reduce((sum, item) => sum + (parseFloat(item.Total) || 0), 0);

  return {
    sheet_name: sheetName,
    title: `${sheetName} - Project Estimate`,
    items: items,
    total: total
  };
}

function processFinancialStatement(data, sheetName) {
  const headers = data[0] || [];
  const rows = data.slice(1);
  
  const sections = [];
  let currentSection = null;
  
  rows.forEach(row => {
    const firstCell = row[0];
    if (firstCell && typeof firstCell === 'string' && firstCell.length > 0) {
      // Check if this looks like a section header
      if (firstCell.toUpperCase() === firstCell || firstCell.includes(':')) {
        if (currentSection) {
          sections.push(currentSection);
        }
        currentSection = {
          name: firstCell,
          items: []
        };
      } else if (currentSection) {
        // Add as item to current section
        const item = {};
        headers.forEach((header, index) => {
          item[header] = row[index];
        });
        currentSection.items.push(item);
      }
    }
  });
  
  if (currentSection) {
    sections.push(currentSection);
  }

  return {
    sheet_name: sheetName,
    title: `${sheetName} - Financial Statement`,
    sections: sections
  };
}
