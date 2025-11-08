from flask import Blueprint, request, jsonify
from app.models.student import Student
from app.services.student_service import add_student, get_all_students, delete_student,update_student
import logging

logger = logging.getLogger(__name__)
student_bp = Blueprint("student", __name__)

@student_bp.route("/students", methods=["POST"])
def create_student():
    """
    Add a new student
    ---
    tags:
      - Students
    parameters:
      - in: body
        name: student
        schema:
          type: object
          required:
            - id
            - name
            - grade
            - subjects
          properties:
            id:
              type: string
            name:
              type: string
            grade:
              type: string
            subjects:
              type: array
              items:
                type: string
    responses:
      201:
        description: Student added successfully
      400:
        description: Duplicate student
      500:
        description: Internal Server Error
    """    
    data = request.get_json()
    logger.info(f"POST /students called with data: {data}")

    subjects_value = ",".join(data["subjects"]) if isinstance(data["subjects"], list) else data["subjects"]

    student = Student(
        id=data["id"],
        name=data["name"],
        grade=data["grade"],
        subjects=subjects_value
    )

    try:
        add_student(student)
        logger.info("Student added successfully")
        return jsonify({"message": "Student added"}), 201
    except ValueError as ve:   # ✅ catch duplicate student error
        logger.error(f"Duplicate student: {ve}")
        return jsonify({"error": str(ve)}), 400   # ✅ return 400 instead of 500
    except Exception as e:
        logger.error(f"Error adding student: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    

@student_bp.route("/students", methods=["GET"])
def get_students():
    """
    Get all students
    ---
    tags:
      - Students
    responses:
      200:
        description: List of students
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              name:
                type: string
              grade:
                type: string
              subjects:
                type: string
      500:
        description: Internal Server Error
    """
    logger.info("GET /students called")
    ...    
    logger.info("GET /students called")
    try:
        students = get_all_students()
        logger.info(f"Fetched {len(students)} students")

        result = [
            {"id": s[0], "name": s[1], "grade": s[2], "subjects": s[3]}
            for s in students
        ]

        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error fetching students: {e}")  
        return jsonify({"error": "Internal Server Error"}), 500


@student_bp.route("/students/<student_id>", methods=["DELETE"])
def remove_student(student_id):
    """
    Delete a student by ID
    ---
    tags:
      - Students
    parameters:
      - in: path
        name: student_id
        type: string
        required: true
    responses:
      200:
        description: Student deleted successfully
      404:
        description: Student not found
      500:
        description: Internal Server Error
    """    
    logger.info(f"DELETE /students/{student_id} called")
    try:
        deleted = delete_student(student_id)   # ✅ check return value
        if not deleted:                       # ✅ student not found
            logger.warning(f"Student with ID {student_id} not found")
            return jsonify({"error": "Student not found"}), 404
        logger.warning(f"Student deleted with ID: {student_id}")
        return jsonify({"message": "Student deleted"}), 200
    except Exception as e:
        logger.error(f"Error deleting student {student_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@student_bp.route("/students/<student_id>", methods=["PUT"])
def update_student_route(student_id):
    """
    Update a student by ID
    ---
    tags:
      - Students
    parameters:
      - in: path
        name: student_id
        type: string
        required: true
      - in: body
        name: student
        schema:
          type: object
          required:
            - name
            - grade
            - subjects
          properties:
            name:
              type: string
            grade:
              type: string
            subjects:
              type: array
              items:
                type: string
    responses:
      200:
        description: Student updated successfully
      404:
        description: Student not found
      500:
        description: Internal Server Error
    """    
    data = request.get_json()
    logger.info(f"PUT /students/{student_id} called with data: {data}")

    subjects_value = ",".join(data["subjects"]) if isinstance(data["subjects"], list) else data["subjects"]

    student = Student(
        id=student_id,   # ✅ keep ID from URL
        name=data["name"],
        grade=data["grade"],
        subjects=subjects_value
    )

    try:
        updated = update_student(student_id, student)   # ✅ call service
        if not updated:
            return jsonify({"error": "Student not found"}), 404   # ✅ return 404
        return jsonify({"message": "Student updated"}), 200       # ✅ return 200
    except Exception as e:
        logger.error(f"Error updating student {student_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
