from typing import List, Optional, Any
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_shema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuariosSchemaArtigos, UsuariosSchemaUp
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso


router = APIRouter()

# GET LOGADO
@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado

# POST / Sign Up
@router.post('/signup', status_code==status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(nome = usuario.nome, sobrenome = usuario.sobrenome, email = usuario.email, senha = gerar_hash_senha(usuario.senha), eh_admin = usuario.eh_admin)
    async with db as session:
        session.add(novo_usuario)
        await session.commit()
        
        return novo_usuario

# GET Usuários
@router.get('/', response_model=List[UsuarioSchemaBase])
async def get_usuarios(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
        
        return usuarios

# GET Usuário
@router.get('/{usuario_id}', response_model=UsuariosSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel.filter(UsuarioModel.id == usuario_id))
        result = await session.execute(query)
        usuario: UsuariosSchemaArtigos = result.scalar().unique().one_or_none()
        
        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        
        
# PUT Usuário
@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def put_usuario(usuario_id: int, usuario: UsuariosSchemaUp,db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel.filter(UsuarioModel.id == usuario_id))
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalar().unique().one_or_none()
        
        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            return usuario_up
        
            if usuario.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            return usuario_up
        
            if usuario.email:
                usuario_up.email = usuario.email
            return usuario_up
        
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)
            return usuario_up
        
            if usuario.eh_admin:
                usuario_up.eh_admin = usuario.eh_admin
            return usuario_up
        
            await session.commit()
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

# DELETE Usuário
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel.filter(UsuarioModel.id == usuario_id))
        result = await session.execute(query)
        usuario_del: UsuariosSchemaArtigos = result.scalar().unique().one_or_none()
        
        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            
            return Reponse(status_code=status.HTTP_404_NOT_FOUND)
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


# POST login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)
    
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')
    
    return JSONResponse(content={"access_token":criar_token_acesso(sub=usuario.id),"token_type":"bearer"}, status_code=status.HTTP_200_OK)
