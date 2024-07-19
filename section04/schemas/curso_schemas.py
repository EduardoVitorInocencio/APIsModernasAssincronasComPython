from typing import Optional, ClassVar

from pydantic_settings import BaseSettings as SCBaseModel #Temos que chamar assim pq o SQL alchemy tem um BaseModel dele


class CursoSchema(SCBaseModel):
    id: Optional[int] #Será criado automaticamente no banco de dados
    titulo: str
    aulas: int
    horas: int
    
    class Config:
        orm_mode = True
        
    