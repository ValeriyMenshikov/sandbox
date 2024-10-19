from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HTTP_API_ACCOUNT: str = "http://5.63.153.31:5051/"
    HTTP_API_LOGIN: str = "http://5.63.153.31:5051/"
    HTTP_MAILHOG: str = "http://5.63.153.31:5025/"
    DISABLE_LOG: bool = False
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_NAME: str = "pomodoro"
    # CACHE_HOST: str = "redis"
    CACHE_HOST: str = "localhost"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0

    @property
    def db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
