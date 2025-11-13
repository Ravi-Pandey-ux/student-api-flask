from .. import db    # ✅ relative import from parent package
from flask_sqlalchemy import SQLAlchemy   # ✅ relative import from parent package
from datetime import datetime

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)   # ✅ integer ID
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(20))
    subjects = db.Column(db.String(200))
