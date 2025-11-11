from flask import Blueprint, request, jsonify
import jwt
import datetime
from functools import wraps


# Create Blueprint
auth_bp = Blueprint("auth", __name__)

# Secret key (later move to config or environment variable)
SECRET_KEY = "super_secret_key"


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

    # Dummy authentication (replace with DB check)
    if username == "ravi" and password == "password123":
        token = jwt.encode(
            {
                "user": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401


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
