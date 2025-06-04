import sqlite3
from datetime import datetime

DB_PATH = "search_history.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table_if_not_exists():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            answer TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_question_column_if_missing():
    conn = get_connection()
    c = conn.cursor()
    c.execute("PRAGMA table_info(searches)")
    columns = [col[1] for col in c.fetchall()]
    if "question" not in columns:
        try:
            c.execute("ALTER TABLE searches ADD COLUMN question TEXT")
            print("Added 'question' column to 'searches' table.")
        except sqlite3.OperationalError as e:
            print("Error adding 'question' column:", e)
    conn.commit()
    conn.close()

def initialize_db():
    create_table_if_not_exists()
    add_question_column_if_missing()

def insert_search(question, answer):
    conn = get_connection()
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO searches (question, answer, timestamp) VALUES (?, ?, ?)", (question, answer, timestamp))
    conn.commit()
    conn.close()

def get_all_searches():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT question, answer, timestamp FROM searches ORDER BY id DESC")
    results = c.fetchall()
    conn.close()
    return results

def clear_history():
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM searches")
    conn.commit()
    conn.close()

initialize_db()
