import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "ibope.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_hash TEXT,
            tipo TEXT,
            data TEXT,
            hora TEXT,
            ddd TEXT,
            is_group INTEGER
        )
    """)

    conn.commit()
    conn.close()
