
"""
Rotas de gerenciamento de usuários.

Responsabilidades:
- Receber requisições relacionadas aos usuários.
- Delegar as regras de negócio para a camada de serviços.
- Disponibilizar operações de cadastro, consulta, atualização
  e remoção de usuários.
- Restringir operações administrativas ao perfil ADMIN.
"""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, require_roles
from app.core.dependencies import get_db
from app.models.user import User
from app.schemas.error import ErrorResponse
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import (
    get_user,
    list_users,
    register_user,
    remove_user,
    update_user_data,
)

router = APIRouter(
    prefix="/users",
    tags=["Usuários"],
)


# ==========================================================
# Cadastro público
# ==========================================================

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar usuário",
    response_description="Usuário cadastrado com sucesso.",
    description="""
Realiza o cadastro público de um novo usuário.

Regras:
- O e-mail informado deve ser único.
- A senha é armazenada utilizando hash.
- O usuário é criado com status ativo.
- O perfil inicial é ALUNO.
- O perfil não pode ser escolhido pelo solicitante.

Este endpoint não requer autenticação.
""",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Dados inválidos.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "E-mail já cadastrado.",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "model": ErrorResponse,
            "description": "Erro de validação.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor.",
        },
    },
)
def criar_usuario(
    usuario: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Cadastra um novo usuário com o perfil ALUNO.
    """

    return register_user(
        db=db,
        user_data=usuario,
    )


# ==========================================================
# Listagem administrativa
# ==========================================================

@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuários",
    response_description="Lista de usuários retornada com sucesso.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Apenas ADMIN pode listar usuários.",
        },
    },
)
def listar_usuarios(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> list[UserResponse]:
    """
    Retorna todos os usuários cadastrados.

    Requer o perfil ADMIN.
    """

    return list_users(db=db)


# ==========================================================
# Dados do próprio usuário
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obter usuário autenticado",
    response_description=(
        "Dados do usuário autenticado retornados com sucesso."
    ),
    description="""
Retorna os dados do usuário associado ao token JWT.

Qualquer usuário autenticado pode consultar os próprios dados.
""",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado ou inativo.",
        },
    },
)
def obter_usuario_logado(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Retorna os dados do usuário autenticado.
    """

    return current_user


# ==========================================================
# Consulta administrativa por identificador
# ==========================================================

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Buscar usuário",
    response_description="Usuário localizado com sucesso.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Apenas ADMIN pode consultar outros usuários.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Usuário não encontrado.",
        },
    },
)
def buscar_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> UserResponse:
    """
    Busca um usuário pelo identificador.

    Requer o perfil ADMIN.
    """

    return get_user(
        db=db,
        user_id=user_id,
    )


# ==========================================================
# Atualização administrativa
# ==========================================================

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Atualizar usuário",
    response_description="Usuário atualizado com sucesso.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Apenas ADMIN pode atualizar usuários.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Usuário não encontrado.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "E-mail já cadastrado.",
        },
    },
)
def atualizar_usuario(
    user_id: int,
    usuario: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> UserResponse:
    """
    Atualiza os dados de um usuário.

    Requer o perfil ADMIN. A alteração do perfil não é
    disponibilizada por meio do schema público de atualização.
    """

    return update_user_data(
        db=db,
        user_id=user_id,
        user_data=usuario,
    )


# ==========================================================
# Remoção administrativa
# ==========================================================

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir usuário",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Apenas ADMIN pode excluir usuários.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Usuário não encontrado.",
        },
    },
)
def excluir_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> Response:
    """
    Remove um usuário do sistema.

    Requer o perfil ADMIN.
    """

    remove_user(
        db=db,
        user_id=user_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
