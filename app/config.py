import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    app_name: str = "Seazone API"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    database_url: str = "postgresql://seazone_user:seazone_password@localhost:5432/seazone_db"
    
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  


settings = Settings()