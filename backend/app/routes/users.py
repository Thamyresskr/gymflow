"""
Rotas de gerenciamento de usuários.

Responsabilidades:
- Cadastro de usuários
- Listagem de usuários
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.dependencies import get_db
from app.crud.user import get_all_users
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import register_user

router = APIRouter(
    prefix="/users",
    tags=["Usuários"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar usuário",
    description="Realiza o cadastro de um novo usuário no sistema.",
)
def criar_usuario(
    usuario: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Cadastra um novo usuário.

    Regras de negócio:
    - O e-mail deve ser único.
    - A senha é armazenada criptografada.
    - O usuário é criado como ALUNO e ativo.

    Todas as regras são executadas pela camada Service.
    """

    return register_user(
        db=db,
        user_data=usuario,
    )


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuários",
    description="Retorna todos os usuários cadastrados. Requer autenticação.",
)
def listar_usuarios(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[UserResponse]:
    """
    Lista todos os usuários cadastrados.

    Requer um JWT válido.
    """

    return get_all_users(db=db)