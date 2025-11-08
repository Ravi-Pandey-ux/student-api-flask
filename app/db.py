import sqlite3

def init_db():
    conn=sqlite3.connect("students.db")
    cursor=conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT,
            grade TEXT,
            subjects TEXT
        )
    """)

    conn.commit
    conn.close
