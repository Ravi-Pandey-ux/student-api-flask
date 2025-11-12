from app import app, db
from app.models.user import User
from app.models.student import Student

def main():
    # Wrap everything inside the app context
    with app.app_context():
        # (1) Print DB path
        print("Database path:", str(db.engine.url))

        # (2) Create tables if missing
        db.create_all()
        print("Tables created (if missing).")

        # (3) List tables
        print("Existing tables:", list(db.metadata.tables.keys()))

if __name__ == "__main__":
    main()
