import json
import requests

# API Gateway endpoint URL
api_gateway_url = "https://vjo7wzkvj7.execute-api.ap-south-1.amazonaws.com/prod"

# Lambda handler function
def lambda_handler(event, context):
    # Extract HTTP method and path from the event
    http_method = event['httpMethod']
    path = event['path']
    
    # Routing based on HTTP method and path
    if http_method == 'GET' and path == '/student':
        return get_students(event)
    elif http_method == 'GET' and path.startswith('/student/'):
        student_id = path.split('/')[-1]
        return get_student(studentid)
    elif http_method == 'POST' and path == '/student':
        return create_student(event)
    elif http_method == 'PUT' and path.startswith('/student/'):
        student_id = path.split('/')[-1]
        return update_student(studentid, event)
    elif http_method == 'DELETE' and path.startswith('/student/'):
        student_id = path.split('/')[-1]
        return delete_student(student_id)
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Endpoint not found'})
        }

# Helper functions for handling API requests

def get_students(event):
    try:
        response = requests.get(api_gateway_url)
        return {
            'statusCode': response.status_code,
            'body': response.json()
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_student(studentid):
    try:
        response = requests.get(f"{api_gateway_url}/{studentid}")
        return {
            'statusCode': response.status_code,
            'body': response.json()
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def create_student(event):
    try:
        data = json.loads(event['body'])
        required_fields = ['studentid', 'fname', 'lname', 'contact', 'email']

        for field in required_fields:
            if field not in data:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'Missing required field: {field}'})
                }

        response = requests.post(api_gateway_url, json=data)
        return {
            'statusCode': response.status_code,
            'body': response.json()
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def update_student(studentid, event):
    try:
        data = json.loads(event['body'])
        required_fields = ['fname', 'lname', 'contact', 'email']

        for field in required_fields:
            if field not in data:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'Missing required field: {field}'})
                }

        response = requests.put(f"{api_gateway_url}/{studentid}", json=data)
        return {
            'statusCode': response.status_code,
            'body': response.json()
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def delete_student(studentid):
    try:
        response = requests.delete(f"{api_gateway_url}/{studentid}")
        return {
            'statusCode': response.status_code,
            'body': response.json()
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
