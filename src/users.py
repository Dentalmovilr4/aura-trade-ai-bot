import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

class UserManager:
    def __init__(self):
        self.conn = sqlite3.connect(os.getenv("DB_PATH"))
        self.create()

    def create(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            api_key TEXT,
            api_secret TEXT,
            balance REAL
        )
        """)

    def add_user(self, name, key, secret, balance):
        self.conn.execute(
            "INSERT INTO users (name, api_key, api_secret, balance) VALUES (?, ?, ?, ?)",
            (name, key, secret, balance)
        )
        self.conn.commit()

    def get_users(self):
        return self.conn.execute("SELECT * FROM users").fetchall()