import pathlib
from typing import ClassVar

from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = pathlib.Path(__file__).parent

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    
    TEST_ENVIRONMENT: str
    MYSQL: str
    TEST_MYSQL: str
    REDIS: str
    TEST_REDIS: str
    BOT_TOKEN: str
    
    
    PRIVATE_KEY: ClassVar[str] = (BASE_DIR / 'keys/private_key.pem').read_text()
    PUBLIC_KEY: ClassVar[str] = (BASE_DIR / 'keys/public_key.pem').read_text()
    
    model_config = SettingsConfigDict(env_file='.env')
    
    
settings = Settings()
