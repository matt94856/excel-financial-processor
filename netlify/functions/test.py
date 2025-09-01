import json

def handler(event, context):
    """Simple test function to verify Netlify routing"""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    }
    
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'message': 'Netlify function is working!',
            'method': event.get('httpMethod', 'UNKNOWN'),
            'path': event.get('path', 'UNKNOWN'),
            'timestamp': str(context.aws_request_id) if context else 'no-context'
        })
    }
