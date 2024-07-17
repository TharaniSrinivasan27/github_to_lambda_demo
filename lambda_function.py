import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# API Gateway endpoint URL
api_gateway_url = "https://vjo7wzkvj7.execute-api.ap-south-1.amazonaws.com/prod"

#to display the students
@app.route('/student', methods=['GET'])
def get_students():
    try:
        response = requests.get(api_gateway_url)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

#to display student by id
@app.route('/student/<student_id>', methods=['GET'])
def get_student(student_id):
    try:
        response = requests.get(f"{api_gateway_url}/{student_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#create a new student
@app.route('/students', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        response = requests.post(api_gateway_url, json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#update the student
@app.route('/student/<student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.get_json()
        response = requests.put(f"{api_gateway_url}/{student_id}", json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#delete the student
@app.route('/student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        response = requests.delete(f"{api_gateway_url}/{student_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
