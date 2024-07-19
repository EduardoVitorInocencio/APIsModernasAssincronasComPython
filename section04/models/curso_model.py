from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy import Column, Integer, String
from pydantic_settings import BaseSettings
from core.configs import settings

from typing import ClassVar

class CursoModel(settings.DBBaseModel):
    __tablename__ = 'cursos'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(100))
    aulas: Mapped[int] = mapped_column(Integer)
    horas: Mapped[int] = mapped_column(Integer)
