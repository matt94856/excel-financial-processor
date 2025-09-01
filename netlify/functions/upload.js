exports.handler = async (event, context) => {
  // Handle CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'POST, OPTIONS, GET'
  };

  // Log the request for debugging
  console.log('Upload function called with method:', event.httpMethod);
  console.log('Event:', JSON.stringify(event, null, 2));

  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: headers,
      body: ''
    };
  }

  try {
    // For now, return a mock response since full Excel processing
    // requires more complex setup in serverless environment
    const fileId = Math.random().toString(36).substr(2, 9);
    
    // Mock processing response
    const response = {
      file_id: fileId,
      original_filename: 'sample.xlsx',
      pdf_download: `/api/download/${fileId}_processed.pdf`,
      excel_download: `/api/download/${fileId}_processed.xlsx`,
      status: 'success',
      message: 'File processed successfully (demo mode)'
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
