import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("trades.db")
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            signal TEXT,
            price REAL
        )
        """)

    def insert(self, symbol, signal, price):
        self.conn.execute(
            "INSERT INTO trades (symbol, signal, price) VALUES (?, ?, ?)",
            (symbol, signal, price)
        )
        self.conn.commit()

    def get_all(self):
        return self.conn.execute("SELECT * FROM trades").fetchall()