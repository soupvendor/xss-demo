from pydantic import BaseModel


class Comment(BaseModel):
    user_id: int
    comment: str


class CommentResponse(Comment):
    id: int


class User(BaseModel):
    username: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str
