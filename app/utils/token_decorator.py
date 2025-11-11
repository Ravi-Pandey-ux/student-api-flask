import jwt
from flask import request,jsonify
from functools import wraps

SECRET_KEY = "super_secret_key"  

def token_required(allowed_roles=None):
    allowed_roles = allowed_roles or []

    def decorator(f):
     @wraps(f)
     def decorated(*args, **kwargs):
          token=request.headers.get("Authorization")
          if not token:
               return jsonify({"message" : "Token missing"}),403
          if token.startswith("Bearer "):
             token = token.split(" ")[1] 

          try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Pass decoded payload to the route
            user_role = decoded.get("role", "user")
            if allowed_roles and user_role not in allowed_roles:
              return jsonify({"message": "Access denied"}), 403
            
            return f(decoded, *args, **kwargs)
          except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
          except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401  

     return decorated                
    return decorator
          
          

