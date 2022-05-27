import sqlite3
from xss_demo.models import User


class Database:
    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.curr = self.conn.cursor()
        self.curr.execute(
            """CREATE TABLE IF NOT EXISTS comments
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            comment TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id))"""
        )
        self.curr.execute(
            """CREATE TABLE IF NOT EXISTS users
            (username TEXT PRIMARY KEY, password TEXT, role TEXT)
            """
        )

    def select_row_by_id(self, id_: int) -> tuple:
        data = self.curr.execute(
            "SELECT * FROM comments WHERE id == ?", (id_,)
        ).fetchone()
        return data

    def select_user(self, user: User) -> tuple:
        data = self.curr.execute(
            "SELECT * FROM users WHERE username == ?", (user.username,)
        ).fetchone()
        response = User(username=data[0], password=data[1], role=data[2])
        return response
