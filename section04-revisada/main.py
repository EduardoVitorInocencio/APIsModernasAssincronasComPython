from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router


app = FastAPI(title='Cursos API - FastAPI SQL Alchemy')
app.include_router(api_router, prefix=settings.API_V1_STR)

# /api/v1/cursos
# /api/v1/usuarios


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level='info', reload=True)
