import sqlite3


def create_connection():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    return c, conn


# sql_db.py
def create_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = c.fetchone()
    if not table_exists:
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
            """
        )

    # Create the passwords table
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='passwords'")
    table_exists = c.fetchone()
    if not table_exists:
        c.execute(
            """
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            storage TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
            """
        )

    conn.commit()
