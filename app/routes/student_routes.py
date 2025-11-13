from flask import Blueprint, request, jsonify
from ..services.student_service import add_student, get_all_students, delete_student, update_student
from ..models.student import Student
from .. import db

import logging
from app.utils.token_decorator import token_required

logger = logging.getLogger(__name__)
student_bp = Blueprint("student", __name__)

# -------------------------
# CREATE STUDENT (Admin only)
# -------------------------
@student_bp.route("/students", methods=["POST"])
@token_required(allowed_roles=["admin"])   # ✅ RBAC enforced
def create_student(decoded_user):
    """
    Add a new student
    """
    data = request.get_json()
    logger.info(f"POST /students called by {decoded_user['user']} with data: {data}")

    subjects_value = ",".join(data["subjects"]) if isinstance(data["subjects"], list) else data["subjects"]

    student = Student(
        name=data["name"],
        grade=data["grade"],
        subjects=subjects_value
    )

    try:
        add_student(student)
        logger.info("Student added successfully")
        return jsonify({
            "message": f"Student added by {decoded_user['user']}",
            "student": {
                "id": student.id,
                "name": student.name,
                "grade": student.grade,
                "subjects": student.subjects
            }
        }), 201
    except ValueError as ve:
        logger.error(f"Duplicate student: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error adding student: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# -------------------------
# GET STUDENTS (Any logged-in user)
# -------------------------
@student_bp.route("/students", methods=["GET"])
@token_required()   # ✅ JWT required, any role allowed
def get_students(decoded_user):
    """
    Get students with pagination
    """
    logger.info(f"GET /students called by {decoded_user['user']}")
    try:
        # ✅ Read query params (defaults: page=1, limit=10)
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)

        # ✅ Paginate query directly from Student model
        students = Student.query.paginate(page=page, per_page=limit, error_out=False)

        logger.info(f"Fetched {len(students.items)} students on page {students.page}")

        # ✅ Format response
        result = [
            {"id": s.id, "name": s.name, "grade": s.grade, "subjects": s.subjects}
            for s in students.items
        ]

        return jsonify({
            "page": students.page,
            "pages": students.pages,
            "total": students.total,
            "per_page": students.per_page,
            "students": result
        }), 200

    except Exception as e:
        logger.error(f"Error fetching students: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# -------------------------
# DELETE STUDENT (Admin only)
# -------------------------
@student_bp.route("/students/<student_id>", methods=["DELETE"])
@token_required(allowed_roles=["admin"])   # ✅ RBAC enforced
def remove_student(decoded_user, student_id):
    """
    Delete a student by ID
    """
    logger.info(f"DELETE /students/{student_id} called by {decoded_user['user']}")
    try:
        deleted = delete_student(student_id)
        if not deleted:
            logger.warning(f"Student with ID {student_id} not found")
            return jsonify({"error": "Student not found"}), 404
        logger.info(f"Student deleted with ID: {student_id}")
        return jsonify({"message": f"Student deleted by {decoded_user['user']}"}), 200
    except Exception as e:
        logger.error(f"Error deleting student {student_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


# -------------------------
# UPDATE STUDENT (Admin only)
# -------------------------
@student_bp.route("/students/<student_id>", methods=["PUT"])
@token_required(allowed_roles=["admin"])   # ✅ RBAC enforced
def update_student_route(decoded_user, student_id):
    """
    Update a student by ID
    """
    data = request.get_json()
    logger.info(f"PUT /students/{student_id} called by {decoded_user['user']} with data: {data}")

    subjects_value = ",".join(data["subjects"]) if isinstance(data["subjects"], list) else data["subjects"]

    student = Student(
        id=student_id,
        name=data["name"],
        grade=data["grade"],
        subjects=subjects_value
    )

    try:
        updated = update_student(student_id, student)
        if not updated:
            logger.warning(f"Student with ID {student_id} not found")
            return jsonify({"error": "Student not found"}), 404
        logger.info(f"Student updated with ID: {student_id}")
        return jsonify({"message": f"Student updated by {decoded_user['user']}"}), 200
    except Exception as e:
        logger.error(f"Error updating student {student_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
