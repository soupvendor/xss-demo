from pydantic import BaseSettings


class Settings(BaseSettings):
    db_path = "../data/demo.db"
    secret_key: str | None

    class Config:
        env_file = ".env"


settings = Settings()
