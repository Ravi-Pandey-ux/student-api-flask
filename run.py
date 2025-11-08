from flask import Flask, g
from flasgger import Swagger
from app.routes.student_routes import student_bp
from app.db import init_db
import logging


logging.basicConfig(
    level=logging.INFO,  # Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),   # Logs to file
        logging.StreamHandler()           # Logs to console
    ]
)
logger = logging.getLogger(__name__)

app=Flask(__name__) 
Swagger(app)
app.register_blueprint(student_bp)

init_db()

@app.route("/")
def home():
    logger.info("Home route accessed")
    return "Welcome to the Student API! Visit /students or /apidocs"

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=5000)
