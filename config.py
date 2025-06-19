from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    SOLANA_RPC_URL: str = "https://api.mainnet-beta.solana.com"
    # DATABASE_URL: str = "sqlite:///./wallets.db"  # або PostgreSQL

    class Config:
        env_file = ".env"


settings = Settings()
