import logging
from flasgger import Swagger
from app import app, db
from app.routes.student_routes import student_bp
from app.routes.auth_routes import auth_bp
from app.models import User, Student

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ✅ Configure database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super_secret_key"

# ✅ Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(student_bp)

# ✅ Swagger docs
Swagger(app)

@app.route("/")
def home():
    logger.info("Home route accessed")
    return "Welcome to the Student API! Visit /students or /apidocs"

# ✅ Create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
