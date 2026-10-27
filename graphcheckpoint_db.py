import sqlite3

DB = "bikehelper.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                answer TEXT NOT NULL,
                source TEXT,
                top_score REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_chat(query, answer, source, score):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "INSERT INTO chats (query, answer, source, top_score) VALUES (?, ?, ?, ?)",
            (query, answer, source, score),
        )

def get_history(limit=10):
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, query, answer, source, created_at FROM chats ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]