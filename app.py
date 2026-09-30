"""In-memory REST API for student records.

Run locally with ``python app.py`` after installing requirements.txt.

Create a student:
    curl -X POST http://127.0.0.1:5000/students \
      -H "Content-Type: application/json" \
      -d '{"name":"Sam Lee","age":21,"major":"Biology","gpa":3.7}'

Delete a student:
    curl -X DELETE http://127.0.0.1:5000/students/1
"""

import math
from itertools import count
from typing import Any

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

students: dict[int, dict[str, Any]] = {
    1: {"id": 1, "name": "Alex Morgan", "age": 20, "major": "Computer Science", "gpa": 3.8},
    2: {"id": 2, "name": "Jordan Lee", "age": 22, "major": "Biology", "gpa": 3.6},
    3: {"id": 3, "name": "Taylor Kim", "age": 19, "major": "Mathematics", "gpa": 3.9},
}
_next_student_id = count(max(students) + 1)
_REQUIRED_FIELDS = {"name", "age", "major", "gpa"}


def error_response(message: str, status: int):
    """Return API errors in the same JSON shape."""
    return jsonify({"error": message}), status


def validate_student_payload(payload: Any) -> tuple[dict[str, Any] | None, str | None]:
    if not isinstance(payload, dict):
        return None, "JSON body must be an object."

    missing = sorted(_REQUIRED_FIELDS - payload.keys())
    if missing:
        return None, f"Missing required field(s): {', '.join(missing)}."

    unexpected = sorted(payload.keys() - _REQUIRED_FIELDS)
    if unexpected:
        return None, f"Unexpected field(s): {', '.join(unexpected)}."

    name = payload["name"]
    major = payload["major"]
    age = payload["age"]
    gpa = payload["gpa"]

    if not isinstance(name, str) or not name.strip():
        return None, "name must be a non-empty string."
    if isinstance(age, bool) or not isinstance(age, int):
        return None, "age must be an integer."
    if not isinstance(major, str) or not major.strip():
        return None, "major must be a non-empty string."
    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        return None, "gpa must be a number."

    normalized_gpa = float(gpa)
    if not math.isfinite(normalized_gpa):
        return None, "gpa must be a finite number."

    return {
        "name": name.strip(),
        "age": age,
        "major": major.strip(),
        "gpa": normalized_gpa,
    }, None


@app.errorhandler(HTTPException)
def handle_http_error(error: HTTPException):
    return error_response(error.description, error.code or 500)


@app.get("/students")
def list_students():
    return jsonify(list(students.values()))


@app.get("/students/<int:student_id>")
def get_student(student_id: int):
    student = students.get(student_id)
    if student is None:
        return error_response("Student not found.", 404)
    return jsonify(student)


@app.post("/students")
def create_student():
    if not request.is_json:
        return error_response("Content-Type must be application/json.", 415)

    payload = request.get_json()
    student_data, validation_error = validate_student_payload(payload)
    if validation_error:
        return error_response(validation_error, 400)

    student_id = next(_next_student_id)
    student = {"id": student_id, **student_data}
    students[student_id] = student
    response = jsonify(student)
    response.status_code = 201
    response.headers["Location"] = f"/students/{student_id}"
    return response


@app.delete("/students/<int:student_id>")
def delete_student(student_id: int):
    if students.pop(student_id, None) is None:
        return error_response("Student not found.", 404)
    return jsonify({"message": "Student deleted successfully."})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
