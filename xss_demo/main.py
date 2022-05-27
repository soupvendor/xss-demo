from fastapi import FastAPI, Depends, HTTPException
from xss_demo.db import Database
from config import settings
from xss_demo.crud import create_comment, retrieve_comment, create_user
from xss_demo.models import Comment, CommentResponse, User
from passlib.context import CryptContext

app = FastAPI()


def get_db():
    yield Database(settings.db_path)


@app.post("/comments/", status_code=200)
def post_comment(comment: Comment, db: Database = Depends(get_db)) -> CommentResponse:
    if not comment.comment:
        raise HTTPException(status_code=400, detail="Do not submit an empty comment!")
    else:
        return create_comment(comment, db)


@app.get("/comments/{comment_id}", status_code=200)
def get_comment(comment_id: int, db: Database = Depends(get_db)) -> CommentResponse:
    data = retrieve_comment(comment_id, db)
    if not data:
        raise HTTPException(status_code=404, detail="No comment found")
    else:
        return data


@app.post("/users/", status_code=200)
def post_user(user: User, db: Database = Depends(get_db)) -> User:
    if user:
        return create_user(user, db)
