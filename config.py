from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    DATABASE_URL: str
    SOLANA_TRACKER_TOKEN: str
    SOLANA_TRACKER_URL: str
    HELIUS_API_KEY: str
    HELIUS_BASE_URL: str
    HELIUS_WEBHOOK_URL: str
    WEBHOOK_ID: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = ".env"


settings = Settings()
