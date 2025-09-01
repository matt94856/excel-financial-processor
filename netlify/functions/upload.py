import json
import base64
import tempfile
import os
import uuid
from pathlib import Path

def handler(event, context):
    """Netlify function to handle Excel file uploads"""
    
    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'POST, OPTIONS, GET'
    }
    
    # Log the request for debugging
    print(f"Upload function called with method: {event.get('httpMethod', 'UNKNOWN')}")
    print(f"Event: {json.dumps(event, default=str)}")
    
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    try:
        # For now, return a mock response since full Excel processing
        # requires more complex setup in serverless environment
        file_id = str(uuid.uuid4())
        
        # Mock processing response
        response = {
            'file_id': file_id,
            'original_filename': 'sample.xlsx',
            'pdf_download': f'/api/download/{file_id}_processed.pdf',
            'excel_download': f'/api/download/{file_id}_processed.xlsx',
            'status': 'success',
            'message': 'File processed successfully (demo mode)'
        }
        
        print(f"Returning response: {response}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response)
        }
        
    except Exception as e:
        error_response = {
            'error': f'Error processing file: {str(e)}'
        }
        print(f"Error occurred: {error_response}")
        
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(error_response)
        }
