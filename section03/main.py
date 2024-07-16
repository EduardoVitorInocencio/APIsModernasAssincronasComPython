from typing     import List, Optional, Any, Dict
from fastapi    import FastAPI
from fastapi    import HTTPException
from fastapi    import status
from fastapi    import Response
from models     import Curso
from fastapi    import Path
from fastapi    import Query
from fastapi    import Header
from fastapi    import Depends

from models import cursos

from time import sleep

def fakeDb ():    
    try:
        print('Abrindo conexão com  banco de dados...')
        sleep(1)
    finally:
        print('Fechando a conexão com o banco de dados...')
        sleep(1)
        

app = FastAPI(
    title = 'API da Geek University',
    version = '0.0.1',
    description = 'API feita para estudos do FASTAPI no Python')


@app.get('/cursos', 
        description = 'Retorna todos os cursos ou uma lista vazia',
        summary = 'Retorna todos os cursos',
        response_model = List[Curso]
         )
async def get_cursos(db: Any = Depends(fakeDb)):
    return cursos


@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path(title='ID do curso', desciption = 'Deve ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fakeDb)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')

@app.post('/cursos', status_code = status.HTTP_201_CREATED, response_model=Curso)
async def post_curso(curso: Optional[Curso] = None):
    next_id: int = len(cursos) + 1
    cursos[next_id] = curso
    del curso.id
    return curso


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso:Curso, db: Any = Depends(fakeDb)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        # curso.id = curso_id
        del curso.id
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')


@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id:int, db: Any = Depends(fakeDb)):
    if curso_id in cursos:
        del cursos[curso_id]
        # return JSONReponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')              

@app.get('/calculadora')
async def calculadora(a: int = Query(default = None, gt=5),b: int = Query(default = None, gt=10) , x_geek: str = Header(default = None),c: Optional[int] = None):
    soma: int = a + b
    
    if c:
        soma = soma + c
        
    print(f'X-GEEK: {x_geek}')
        
    return {"resultado": soma}


if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload = True)