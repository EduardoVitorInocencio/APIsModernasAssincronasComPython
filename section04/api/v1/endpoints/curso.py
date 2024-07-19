from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException,status
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CursoModel
from schemas.curso_schemas import CursoSchema
from core.deps import get_session


router = APIRouter()

# Endpoint para permitir a criação de um novo curso. Injeção de dependências
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoSchema)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(
                            titulo = curso.titulo,
                            aulas = curso.aulas,
                            horas = curso.horas
                            )
    
    db.add(novo_curso)
    await db.commit()
    
    return novo_curso  


#GET Cursos
@router.get('/',response_model = List[CursoSchema])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()
        
        return cursos
    

#GET curso
@router.get('/{curso_id}', response_model=CursoSchema, status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()
        
        if curso:
            return curso
        else:
            raise HTTPException(detail='Curso não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)

#PUT curso
@router.put('/{curso_id}', response_model = CursoSchema, status_code = status.HTTP_202_ACCEPTED)
async def put_curso(curso_id: int,curso:CursoSchema,  db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_up = result.scalar_one_or_none()
        
        if curso:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas
            
            await session.commit()
            
            return curso_up
        else:
            raise HTTPException(detail='Curso não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)
            
# DELETE curso

@router.delete('/{curso_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int,  db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_del = result.scalar_one_or_none()
        
        if curso:
            curso_del.titulo = curso.titulo
            curso_del.aulas = curso.aulas
            curso_del.horas = curso.horas
            
            await session.commit()
            
            return curso_del
        else:
            raise HTTPException(detail='Curso não encontrado.',
                                status_code=status.HTTP_404_NOT_FOUND)