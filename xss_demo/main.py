from fastapi import FastAPI
from db import Database
from config import settings

app = FastAPI()

def get_db():
    yield Database(settings.db_path)





@app.post("/comments/", status_code=200)
def create_comment():
    pass


@app.get("/comments/{comment_id}", stauts_code=200)
def get_comment():
    pass

