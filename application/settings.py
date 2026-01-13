from pydantic_settings import BaseSettings

# BASE_HOST = "5.63.153.31"
BASE_HOST = "185.185.143.231"

class Settings(BaseSettings):
    HTTP_API_ACCOUNT: str = f"http://{BASE_HOST}:5051/"
    HTTP_API_LOGIN: str = f"http://{BASE_HOST}:5051/"
    HTTP_API_FORUM: str = f"http://{BASE_HOST}:5051/"
    HTTP_MAILHOG: str = f"http://{BASE_HOST}:5025/"
    DISABLE_LOG: bool = False
    # DB_HOST: str = "postgres"
    DB_HOST: str = BASE_HOST
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "admin"
    DB_DRIVER: str = "postgresql+asyncpg"
    DB_NAME: str = "dm3.5"
    CACHE_HOST: str = "redis-sandbox"
    # CACHE_HOST: str = "localhost"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    # CH_HOST: str = "localhost"
    # CH_HOST: str = "clickhouse-sandbox"
    CH_HOST: str = BASE_HOST
    CH_PORT: int = 8123
    CH_DB: str = "sandbox"
    CH_USER: str = ""
    CH_PASSWORD: str = ""
    MAIL_FROM: str = '"DM.am" <info@dm.am>'
    SMTP_HOST: str = BASE_HOST
    SMTP_PORT: int = 1025
    SMTP_PASSWORD: str = ""
    KAFKA_URL: str = "kafka:19092"
    # KAFKA_URL: str = f"{BASE_HOST}:9092"
    # KAFKA_URL: str = "localhost:9092"
    KAFKA_REGISTER_TOPIC: str = "register-events"
    KAFKA_REGISTER_TOPIC_ERROR: str = "register-events-errors"

    @property
    def db_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def ch_url(self) -> str:
        return f"http://{self.CH_HOST}:{self.CH_PORT}/"
