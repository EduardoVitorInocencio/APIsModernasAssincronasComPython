from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from typing import ClassVar

class Settings(BaseSettings):
    """
        Configurações gerais usadas em nossa aplicação
    
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:DataMastery@localhost:5432/faculdade"
    DBBaseModel : ClassVar = declarative_base()
    
    class Config:
        case_sensitive = True
        from_attributes = True

settings = Settings()
    