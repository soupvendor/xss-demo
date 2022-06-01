from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from xss_demo.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    oauth2_scheme,
)
from xss_demo.config import settings
from xss_demo.crud import create_comment, create_user, list_comments, retrieve_comment
from xss_demo.db import Database, get_db
from xss_demo.models import Comment, CommentResponse, Token, User

app = FastAPI()


@app.post("/comments/", status_code=200)
def post_comment(comment: Comment, db: Database = Depends(get_db)) -> CommentResponse:
    if not comment.comment:
        raise HTTPException(status_code=400, detail="Do not submit an empty comment!")
    else:
        return create_comment(comment, db)


@app.get("/comments/{comment_id}/", status_code=200)
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


@app.post("/token/", response_model=Token)
def get_login_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Database = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expires_minutes)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    # response = JSONResponse(content={})
    # response.set_cookie(key="session", value=access_token)
    # return response
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/comments/")
def list_all_comments(token: str = Depends(oauth2_scheme), db: Database = Depends(get_db)):
    return list_comments(db)


@app.post("/cookie/")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response


@app.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
