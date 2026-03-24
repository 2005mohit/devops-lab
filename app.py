from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database"
students = [
    {"id": 1, "name": "Alice", "grade": "A"},
    {"id": 2, "name": "Bob",   "grade": "B"},
]

@app.route('/')
def home():
    return jsonify({"message": "DevOps Lab API is running!"})

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student), 200
    return jsonify({"error": "Student not found"}), 404

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or "name" not in data or "grade" not in data:
        return jsonify({"error": "Invalid data"}), 400
    new_student = {"id": len(students) + 1, "name": data["name"], "grade": data["grade"]}
    students.append(new_student)
    return jsonify(new_student), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)