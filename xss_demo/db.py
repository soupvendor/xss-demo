import sqlite3
from config import settings

class Database:
    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.curr = self.conn.cursor()
        self.curr.execute(
            """CREATE TABLE IF NOT EXISTS comments
            (id INTEGER PRIMARY KEY AUTOINCREMENT, comment TEXT, user_id INTEGER)"""
            )
        # self.curr.execute(
        #     """CREATE TABLE IF NOT EXISTS users
        #     (id INTEGER PRIMARY KEY AUTOINCREMENT, )
        #     """
        # )
