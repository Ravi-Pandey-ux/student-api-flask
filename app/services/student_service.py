import sqlite3
from flask import g
import logging
from app.models.student import Student  
logger = logging.getLogger(__name__)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("students.db", check_same_thread=False, timeout=10)
    return g.db

def add_student(student: Student):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO students (id, name, grade, subjects) VALUES (?, ?, ?, ?)",
            (student.id, student.name, student.grade, student.subjects)
        )
        db.commit()
        logger.info(f"Student added: {student.name} (Id {student.id})")
    except sqlite3.IntegrityError as e:   # Catch duplicate ID error
        logger.error(f"Duplicate student error: {e}")
        raise ValueError("Student already exists") from e   
    except Exception as e:
        logger.error(f"Error adding student: {e}")
        raise

def get_all_students():
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        logger.info(f"Fetched {len(students)} students from DB")
        return students
    except Exception as e:
        logger.error(f"Error fetching students: {e}")
        raise        

def delete_student(student_id: str):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        db.commit()
        if cursor.rowcount == 0:   
            logger.warning(f"Student with ID {student_id} not found")
            return False           
        logger.warning(f"Deleted student with ID: {student_id}")
        return True               
    except Exception as e:
        logger.error(f"Error deleting student {student_id}: {e}")
        raise


def update_student(student_id: str, student: Student):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE students SET name=?, grade=?, subjects=? WHERE id=?",
            (student.name, student.grade, student.subjects, student_id)
        )
        db.commit()
        if cursor.rowcount == 0:   # ✅ no student updated
            logger.warning(f"Student with ID {student_id} not found")
            return False           # ✅ signal not found
        logger.info(f"Updated student with ID: {student_id}")
        return True                # ✅ signal success
    except Exception as e:
        logger.error(f"Error updating student {student_id}: {e}")
        raise
