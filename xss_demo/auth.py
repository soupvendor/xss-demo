from passlib.context import CryptContext
from xss_demo.db import Database
from xss_demo.models import User
from config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def authenticate_user(user: User, db: Database):
    user = db.select_user(user.username)
    if not user:
        return False
    if not verify_password(user.password, user.hashed_password):
        return False
    return user