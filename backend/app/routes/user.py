from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.user import UserCreate

from app.core.dependencies import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/")
def criar_usuario(
    usuario: UserCreate,
    db: Session = Depends(get_db)
):
    novo_usuario = User(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=usuario.senha,
        tipo="aluno"
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {
        "id": novo_usuario.id,
        "nome": novo_usuario.nome,
        "email": novo_usuario.email
    }


@router.get("/")
def listar_usuarios(
    db: Session = Depends(get_db)
):
    usuarios = db.query(User).all()

    return usuarios