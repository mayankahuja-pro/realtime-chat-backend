from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool

    HOST: str
    PORT: int

    DATABASE_URL: str
    REFRESH_TOKEN_EXPIRE_DAYS: int
    SECRET_KEY: str
    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int = 0

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()