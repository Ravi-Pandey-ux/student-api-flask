from app import db
from app.models.student import Student
import logging

logger = logging.getLogger(__name__)

def add_student(student: Student):
    # try:
    #     existing = Student.query.filter_by(id=student.id).first()
    #     if existing:
    #         raise ValueError("Student already exists")

        db.session.add(student)
        db.session.commit()
        logger.info(f"Student added: {student.name} (Id {student.id})")
        return True
    # except Exception as e:
    #     db.session.rollback()
    #     logger.error(f"Error adding student: {e}")
    #     raise

def get_all_students():
    return Student.query.all()

def delete_student(student_id: int):
    student = Student.query.get(student_id)
    if not student:
        return False
    db.session.delete(student)
    db.session.commit()
    return True

def update_student(student_id: int, student: Student):
    existing = Student.query.get(student_id)
    if not existing:
        return False
    existing.name = student.name
    existing.grade = student.grade
    existing.subjects = student.subjects
    db.session.commit()
    return True
