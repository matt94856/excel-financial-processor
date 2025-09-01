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
    
    // For demo purposes, return a simple response
    // In production, you'd serve the actual generated file
    let contentType, mockContent;
    
    if (filename.endsWith('.pdf')) {
      contentType = 'application/pdf';
      // Mock PDF content (in real implementation, you'd return actual PDF)
      mockContent = Buffer.from('%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Excel Financial Processor Demo) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF');
    } else {
      contentType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
      // Mock Excel content
      mockContent = Buffer.from('PK\x03\x04\x14\x00\x00\x00\x08\x00\x00\x00\x00\x00Demo Excel File');
    }
    
    return {
      statusCode: 200,
      headers: {
        ...headers,
        'Content-Type': contentType,
        'Content-Disposition': `attachment; filename="${filename}"`
      },
      body: mockContent.toString('base64'),
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
