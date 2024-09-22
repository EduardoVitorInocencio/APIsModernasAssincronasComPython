from typing import List

from pydantic_settings import BaseSettings # Permite a importação de uma configuração base para gerar as apis

# from pydantic import BaseSettings 
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:DataMastery@localhost:5432/faculdade'
    
    JWT_SECRET: str ='gKAj01dwh-SgA48gAHyhFak8H4iRf86p4vr87VE1xL8'
    
    """
        import secrets
        
        token: str = secrets.token_urlsafe(32)
        Utilizado para Gerar os tokens de segurança
    """
    
    ALGORITHM: str = 'HS256'
    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    

    class Config:
        case_sensitive = True
        
settings: Settings = Settings()
    
    
    