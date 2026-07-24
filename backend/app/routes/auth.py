"""
Rotas relacionadas à autenticação.

Responsabilidades:
- Receber requisições de autenticação
- Delegar regras de negócio para a camada Service
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.auth import Token
from app.services.auth_service import login_user

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


@router.post(
    "/login",
    response_model=Token,
    summary="Realizar login",
    description="Autentica um usuário e retorna um token JWT.",
    responses={
        200: {"description": "Login realizado com sucesso."},
        401: {"description": "E-mail ou senha inválidos."},
    },
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """
    Autentica um usuário utilizando e-mail e senha.

    Todas as regras de autenticação são executadas
    pela camada Service.
    """

    return login_user(
        db=db,
        email=form_data.username,
        senha=form_data.password,
    )