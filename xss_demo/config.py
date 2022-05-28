from pydantic import BaseSettings


class Settings(BaseSettings):
    db_path = "data/demo.db"
    secret_key: str
    access_token_expires_minutes: int
    algorithm = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
