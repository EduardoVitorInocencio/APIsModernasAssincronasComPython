from typing     import List, Optional
from fastapi    import FastAPI
from fastapi    import HTTPException
from fastapi    import status
from fastapi    import Response
from models     import Curso
from fastapi    import Path
from fastapi    import Query

app = FastAPI()

cursos = {
    1:{
        "título":"Power BI Básico",
        "aulas" : "112",
        "horas" : 58
    },
    
    2:{
        "título":"Python Módulo 01",
        "aulas" : "150",
        "horas" : 125
    }
}

@app.get('/cursos')
async def get_cursos():
    return cursos


@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path(title='ID do curso', desciption = 'Deve ser entre 1 e 2', gt=0, lt=3)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')

@app.post('/cursos', status_code = status.HTTP_201_CREATED)
async def post_curso(curso: Optional[Curso] = None):
    next_id: int = len(cursos) + 1
    cursos[next_id] = curso
    del curso.id
    return curso


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso:Curso):
    if curso_id in cursos:
        cursos[curso_id] = curso
        # curso.id = curso_id
        del curso.id
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')


@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id:int):
    if curso_id in cursos:
        del cursos[curso_id]
        # return JSONReponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado')              

@app.get('/calculadora')
async def calculadora(a: int = Query(default = None, gt=5),b: int = Query(default = None, gt=10) ,c: Optional[int] = None):
    soma: int = a + b
    
    if c:
        soma = soma + c
        
    return {"resultado": soma}


if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload = True)