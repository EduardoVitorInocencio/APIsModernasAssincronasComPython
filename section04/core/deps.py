from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session

async def get_session() -> Generator:
    session: AsyncSession = Session()
    
    try:
        yield session #abre a conexão com o banco de dados e mantém aberta
    finally:
        await session.close() #após consumir a conexão, fechamos após o uso
        
        
        