from typing import Optional
from typing import List
from pydantic import BaseModel, EmailStr

from pydantic_settings import BaseSettings as SCBaseModel

from schemas.artigo_schema import ArtigoSchema

class UsuarioSchemaBase (SCBaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False
    
    class Config:
        orm_mode = True
        

class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha:str
    

class UsuariosSchemaArtigos(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]
    
class UsuariosSchemaUp(UsuarioSchemaBase):
    nome: Optiona[str]
    sobrenome: Optional[str]
    email: Optional[str]
    senha: Optional[str]
    eh_admin: Optional[bool]
    