from typing import Optional
from pydantic import BaseModel, validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int
    
    @validator('titulo')
    def validar_titulo(cls, value):
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O título deve ter pelo menos três palavras')
        
        if value.islower():
            raise ValueError('O nome deve ser escrito em letras maiúsculas')
        
        return value
    
    @validator('aulas')
    def validar_aulas(cls, value):
        if value <= 0:
            raise ValueError('Digite um valor maior que 0.')
        
        if value >= 200:
            raise ValueError('Digite até 200.')
        
        return value
    
    @validator('horas')
    def validar_aulas(cls, value):
        if value <= 0:
            raise ValueError('Digite um valor maior que 0.')
        
        if value >= 400:
            raise ValueError('Digite até 400.')
        
        return value
    
cursos = [
    Curso(id=1, titulo = 'Programação para leigos', aulas = 42, horas = 56),
    Curso(id=2, titulo = 'Java Fundamentos de Programação', aulas = 25, horas = 50),
    Curso(id=3, titulo = 'Power BI Básico', aulas = 42, horas = 56)
]