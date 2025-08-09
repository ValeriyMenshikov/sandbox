from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HTTP_API_ACCOUNT: str = "http://5.63.153.31:5051/"
    HTTP_API_LOGIN: str = "http://5.63.153.31:5051/"
    HTTP_API_FORUM: str = "http://5.63.153.31:5051/"
    HTTP_MAILHOG: str = "http://5.63.153.31:5025/"
    DISABLE_LOG: bool = False
    # DB_HOST: str = "postgres"
    DB_HOST: str = "5.63.153.31"
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
    CH_HOST: str = "clickhouse-sandbox"
    # CH_HOST: str = "5.63.153.31"
    CH_PORT: int = 8123
    CH_DB: str = "sandbox"
    CH_USER: str = ""
    CH_PASSWORD: str = ""
    MAIL_FROM: str = '"DM.am" <info@dm.am>'
    SMTP_HOST: str = "5.63.153.31"
    SMTP_PORT: int = 1025
    SMTP_PASSWORD: str = ""
    # KAFKA_URL: str = "kafka:19092"
    KAFKA_URL: str = "5.63.153.31:9092"
    # KAFKA_URL: str = "localhost:9092"
    KAFKA_REGISTER_TOPIC: str = "register-events"
    KAFKA_REGISTER_TOPIC_ERROR: str = "register-events-errors"

    @property
    def db_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def ch_url(self) -> str:
        return f"http://{self.CH_HOST}:{self.CH_PORT}/"
