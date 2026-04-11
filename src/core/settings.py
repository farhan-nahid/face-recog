from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # AWS Credentials
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_STS_DURATION_SECONDS: int

    # Database
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int

    # App
    PORT: int
    LOG_LEVEL: str
    ENVIRONMENT: str
    CORS_ALLOWED_ORIGINS: str

    # Hr API
    HR_API_URL: str
    HR_API_TOKEN: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
