import pathlib
from typing import ClassVar

from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = pathlib.Path(__file__).parent

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    
    # Environment type
    TEST_ENVIRONMENT: str
    
    # MySQL database URLs
    MYSQL: str
    TEST_MYSQL: str
    
    # Redis database URLs
    REDIS: str
    TEST_REDIS: str
    
    # Telegram bot token
    BOT_TOKEN: str
    
    # mailget credentials
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    
    # https://api.exchangerate.host/
    EXCHANGERATE_API_KEY: str
    
    # Google cloud
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_CLIENT_ID: str
    
    # .pem keys for jwt tokens (not from .env)
    PRIVATE_KEY: ClassVar[str] = (BASE_DIR / 'keys/private_key.pem').read_text()
    PUBLIC_KEY: ClassVar[str] = (BASE_DIR / 'keys/public_key.pem').read_text()
    
    model_config = SettingsConfigDict(env_file='.env')
    
    
settings = Settings()
