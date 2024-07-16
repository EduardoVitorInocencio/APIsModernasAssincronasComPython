from typing import Optional
from pydantic import BaseModel


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int
    
cursos = [
    Curso(id=1, titulo = 'Programação para leigos', aulas = 42, horas = 56),
    Curso(id=2, titulo = 'Java', aulas = 25, horas = 50),
    Curso(id=3, titulo = 'Power BI', aulas = 42, horas = 56)
]