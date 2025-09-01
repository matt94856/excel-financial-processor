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
  
  return {
    statusCode: 200,
    headers: headers,
    body: JSON.stringify({
      status: 'healthy',
      service: 'Excel Financial Processor',
      version: '1.0.0',
      environment: 'JavaScript'
    })
  };
};
