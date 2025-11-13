from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Health route (optional)
@app.get("/")
def health():
    return jsonify({"status": "ok"}), 200

# Import and register your existing routes
from .routes.auth_routes import auth_bp
from .routes.student_routes import student_bp

# Choose one style:
app.register_blueprint(auth_bp)              # → /auth/signup, /auth/login
app.register_blueprint(student_bp)           # → /students

# OR with prefix:
# app.register_blueprint(auth_bp, url_prefix="/api")      # → /api/auth/signup
# app.register_blueprint(student_bp, url_prefix="/api")   # → /api/students
