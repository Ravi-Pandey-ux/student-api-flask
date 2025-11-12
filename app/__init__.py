from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'

db = SQLAlchemy(app)

# Import models so they register
from app.models.user import User
from app.models.student import Student

__all__ = ["app", "db"]
