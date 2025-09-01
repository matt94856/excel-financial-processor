const XLSX = require('xlsx');
const { jsPDF } = require('jspdf');
require('jspdf-autotable');

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS'
  };
  
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: headers,
      body: ''
    };
  }
  
  try {
    // Extract filename from path
    const path = event.path || '';
    const filename = path.split('/').pop() || 'sample.xlsx';
    const fileId = filename.split('_')[0];
    
    // In a real application, you'd retrieve the processed data from a database
    // For now, we'll generate sample data based on the file type
    let contentType, fileContent;
    
    if (filename.endsWith('.pdf')) {
      contentType = 'application/pdf';
      fileContent = generatePDF(fileId);
    } else {
      contentType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
      fileContent = generateExcel(fileId);
    }
    
    return {
      statusCode: 200,
      headers: {
        ...headers,
        'Content-Type': contentType,
        'Content-Disposition': `attachment; filename="${filename}"`
      },
      body: fileContent.toString('base64'),
      isBase64Encoded: true
    };
    
  } catch (error) {
    return {
      statusCode: 500,
      headers: headers,
      body: JSON.stringify({
        error: `Error downloading file: ${error.message}`
      })
    };
  }
};

function generatePDF(fileId) {
  const doc = new jsPDF();
  
  // Add title
  doc.setFontSize(20);
  doc.setFont(undefined, 'bold');
  doc.text('Excel Financial Processor', 20, 30);
  doc.setFontSize(12);
  doc.setFont(undefined, 'normal');
  doc.text('Professional Document Generation', 20, 40);
  
  // Add sample estimate section
  doc.setFontSize(16);
  doc.setFont(undefined, 'bold');
  doc.text('Project Estimate', 20, 60);
  
  // Sample estimate data
  const estimateData = [
    ['Project', 'Hours', 'Rate', 'Total'],
    ['Website Development', '120', '$100', '$12,000'],
    ['Mobile App', '200', '$120', '$24,000'],
    ['Database Design', '80', '$90', '$7,200'],
    ['API Integration', '60', '$110', '$6,600'],
    ['Testing', '40', '$80', '$3,200'],
    ['Deployment', '20', '$100', '$2,000']
  ];
  
  // Add table
  doc.autoTable({
    startY: 70,
    head: [estimateData[0]],
    body: estimateData.slice(1),
    styles: {
      fontSize: 10,
      cellPadding: 5
    },
    headStyles: {
      fillColor: [54, 96, 146],
      textColor: 255,
      fontStyle: 'bold'
    },
    alternateRowStyles: {
      fillColor: [248, 249, 250]
    }
  });
  
  // Add total
  const finalY = doc.lastAutoTable.finalY + 10;
  doc.setFont(undefined, 'bold');
  doc.text('Total Project Cost: $55,000', 20, finalY);
  
  // Add financial statement section
  doc.addPage();
  doc.setFontSize(16);
  doc.setFont(undefined, 'bold');
  doc.text('Financial Statement', 20, 30);
  
  // Sample financial data
  const financialData = [
    ['Description', 'Amount'],
    ['REVENUE', ''],
    ['Project Revenue', '$55,000'],
    ['Consulting Fees', '$15,000'],
    ['TOTAL REVENUE', '$70,000'],
    ['', ''],
    ['EXPENSES', ''],
    ['Development Costs', '$25,000'],
    ['Marketing', '$5,000'],
    ['Administrative', '$3,000'],
    ['TOTAL EXPENSES', '$33,000'],
    ['', ''],
    ['NET INCOME', '$37,000']
  ];
  
  doc.autoTable({
    startY: 40,
    body: financialData,
    styles: {
      fontSize: 10,
      cellPadding: 5
    },
    bodyStyles: {
      fillColor: [255, 255, 255]
    },
    didParseCell: function(data) {
      if (data.row.index === 0 || data.row.index === 4 || data.row.index === 5 || data.row.index === 10 || data.row.index === 11 || data.row.index === 12) {
        data.cell.styles.fillColor = [54, 96, 146];
        data.cell.styles.textColor = 255;
        data.cell.styles.fontStyle = 'bold';
      }
    }
  });
  
  return Buffer.from(doc.output('arraybuffer'));
}

function generateExcel(fileId) {
  const workbook = XLSX.utils.book_new();
  
  // Create summary sheet
  const summaryData = [
    ['FINANCIAL DOCUMENT PROCESSOR - SUMMARY'],
    [''],
    ['Source File: sample_mixed.xlsx'],
    [''],
    ['Total Estimates', '1'],
    ['Total Financial Statements', '1'],
    ['Total Sheets Processed', '2'],
    ['Grand Total', '$55,000']
  ];
  
  const summarySheet = XLSX.utils.aoa_to_sheet(summaryData);
  XLSX.utils.book_append_sheet(workbook, summarySheet, 'Summary');
  
  // Create formatted estimate sheet
  const estimateData = [
    ['Project Estimate - Formatted'],
    [''],
    ['Description', 'Hours', 'Rate', 'Total'],
    ['Website Development', 120, 100, 12000],
    ['Mobile App', 200, 120, 24000],
    ['Database Design', 80, 90, 7200],
    ['API Integration', 60, 110, 6600],
    ['Testing', 40, 80, 3200],
    ['Deployment', 20, 100, 2000],
    ['', '', 'TOTAL:', 55000]
  ];
  
  const estimateSheet = XLSX.utils.aoa_to_sheet(estimateData);
  
  // Add formatting
  const range = XLSX.utils.decode_range(estimateSheet['!ref']);
  for (let row = range.s.r; row <= range.e.r; row++) {
    for (let col = range.s.c; col <= range.e.c; col++) {
      const cellAddress = XLSX.utils.encode_cell({ r: row, c: col });
      if (!estimateSheet[cellAddress]) continue;
      
      if (row === 0) {
        estimateSheet[cellAddress].s = { font: { bold: true, size: 14 }, fill: { fgColor: { rgb: "366092" } } };
      } else if (row === 2) {
        estimateSheet[cellAddress].s = { font: { bold: true }, fill: { fgColor: { rgb: "366092" } } };
      } else if (row === estimateData.length - 1 && col >= 2) {
        estimateSheet[cellAddress].s = { font: { bold: true }, fill: { fgColor: { rgb: "D9E2F3" } } };
      }
    }
  }
  
  XLSX.utils.book_append_sheet(workbook, estimateSheet, 'Estimate_Formatted');
  
  // Create financial statement sheet
  const financialData = [
    ['Financial Statement - Formatted'],
    [''],
    ['REVENUE'],
    ['Description', 'Amount'],
    ['Project Revenue', 55000],
    ['Consulting Fees', 15000],
    ['TOTAL REVENUE', 70000],
    [''],
    ['EXPENSES'],
    ['Description', 'Amount'],
    ['Development Costs', 25000],
    ['Marketing', 5000],
    ['Administrative', 3000],
    ['TOTAL EXPENSES', 33000],
    [''],
    ['NET INCOME', 37000]
  ];
  
  const financialSheet = XLSX.utils.aoa_to_sheet(financialData);
  XLSX.utils.book_append_sheet(workbook, financialSheet, 'Financial_Formatted');
  
  return Buffer.from(XLSX.write(workbook, { type: 'buffer', bookType: 'xlsx' }));
}
