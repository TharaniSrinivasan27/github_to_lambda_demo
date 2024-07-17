
from flask import Flask, request, jsonify

app = Flask(__name__)

# API Gateway endpoint URL
api_gateway_url = "https://vjo7wzkvj7.execute-api.ap-south-1.amazonaws.com/prod"

# Display all students
@app.route('/student', methods=['GET'])
def get_students():
    try:
        response = request.get(api_gateway_url)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Display a specific student by ID
@app.route('/student/<studentid>', methods=['GET'])
def get_student(studentid):
    try:
        response = request.get(f"{api_gateway_url}/{studentid}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create a new student
@app.route('/student', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        required_fields = ['studentid', 'fname', 'lname', 'contact', 'email']  # Define required fields

        # Check if all required fields are present
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Send POST request to API Gateway URL
        response = request.post(api_gateway_url, json=data)
        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update a student by ID
@app.route('/student/<studentid>', methods=['PUT'])
def update_student(studentid):
    try:
        data = request.get_json()
        required_fields = ['fname', 'lname', 'contact', 'email']  # Define required fields for update

        # Check if all required fields are present
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Send PUT request to API Gateway URL
        response = request.put(f"{api_gateway_url}/{studentid}", json=data)
        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a student by ID
@app.route('/student/<studentid>', methods=['DELETE'])
def delete_student(studentid):
    try:
        response = request.delete(f"{api_gateway_url}/{studentid}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
