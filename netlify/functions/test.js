exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
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
      message: 'Netlify function is working!',
      method: event.httpMethod || 'UNKNOWN',
      path: event.path || 'UNKNOWN',
      timestamp: context.awsRequestId || 'no-context',
      environment: 'JavaScript'
    })
  };
};
