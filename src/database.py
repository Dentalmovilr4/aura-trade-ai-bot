import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("trading.db")
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signal TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

    def insert(self, signal):
        self.conn.execute("INSERT INTO signals (signal) VALUES (?)", (signal,))
        self.conn.commit()