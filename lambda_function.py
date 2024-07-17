import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('index')  # Replace 'index' with your DynamoDB table name

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
        return get_student(student_id)
    elif http_method == 'POST' and path == '/student':
        return create_student(event)
    elif http_method == 'PUT' and path.startswith('/student/'):
        student_id = path.split('/')[-1]
        return update_student(student_id, event)
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
        # Example: Fetch all items from DynamoDB table
        response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_student(student_id):
    try:
        # Example: Fetch item from DynamoDB by student_id
        response = table.get_item(Key={'studentid': student_id})
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Student not found'})
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

        # Example: Insert item into DynamoDB table
        table.put_item(Item=data)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Student created successfully', 'student': data})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def update_student(student_id, event):
    try:
        data = json.loads(event['body'])
        required_fields = ['fname', 'lname', 'contact', 'email']

        for field in required_fields:
            if field not in data:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'Missing required field: {field}'})
                }

        # Example: Update item in DynamoDB table
        table.update_item(
            Key={'studentid': student_id},
            UpdateExpression='SET fname = :f, lname = :l, contact = :c, email = :e',
            ExpressionAttributeValues={
                ':f': data['fname'],
                ':l': data['lname'],
                ':c': data['contact'],
                ':e': data['email']
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Student updated successfully', 'student_id': student_id, 'updated_fields': data})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def delete_student(student_id):
    try:
        # Example: Delete item from DynamoDB table
        table.delete_item(Key={'studentid': student_id})

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Student deleted successfully', 'student_id': student_id})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
