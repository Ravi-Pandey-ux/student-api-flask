from flask import Blueprint, request, jsonify
import jwt,datetime
from functools import wraps
from app.models.user import User, db


# Create Blueprint
auth_bp = Blueprint("auth", __name__)

# Secret key (later move to config or environment variable)
SECRET_KEY = "super_secret_key"
@auth_bp.route("/signup", methods=["POST"])
def signup():
    """
    Signup route: creates a new user with hashed password and role.
    Body: { "username": "...", "password": "...", "role": "admin|user" }
    """ 
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")
    role= data.get("role","user") 

    if not username or not password:
        return jsonify({"error" : "username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400 
    
    new_user = User(username=username, role=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()    

    return jsonify({"message": f"User {username} created successfully with role {role}"}), 201




# -------------------------
# LOGIN ROUTE
# -------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login route: validates user and returns JWT token.
    Replace dummy check with DB lookup later.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401 
     
    token = jwt.encode(
# Dummy authentication (replace with DB check)
        {
            "user": user.username,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return jsonify({"token": token})


# -------------------------
# PROTECTED ROUTE
# -------------------------
@auth_bp.route("/protected", methods=["GET"])
def protected():
    """
    Protected route: requires valid JWT token.
    """
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token missing"}), 403

    # ✅ Fix: Strip "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"message": f"Welcome {decoded['user']}!"})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401
