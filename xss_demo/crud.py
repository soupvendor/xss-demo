from xss_demo.db import Database
from xss_demo.models import Comment, CommentResponse, User
from xss_demo.auth import get_password_hash


def create_comment(comment: Comment, db: Database) -> CommentResponse:
    db.curr.execute(
        """INSERT INTO comments
        (user_id, comment)
        VALUES (?, ?)""",
        (comment.user_id, comment.comment),
    )
    db.conn.commit()
    new_id = db.curr.lastrowid
    response = CommentResponse(
        user_id=comment.user_id, comment=comment.comment, id=new_id
    )
    return response


def retrieve_comment(id_: int, db: Database) -> CommentResponse:
    data = db.select_row_by_id(id_)
    response = CommentResponse(user_id=data[1], comment=data[2], id=id_)
    return response


def create_user(user: User, db: Database) -> User:
    hashed_pw = get_password_hash(user.password)
    db.curr.execute(
        """INSERT INTO users
        (username, password, role)
        VALUES (?, ?, ?)""",
        (user.username, hashed_pw, user.role),
    )
    db.conn.commit()
    new_user = db.select_user(user)
    response = User(username=new_user[0], password=new_user[1], role=new_user[2])
    return response
