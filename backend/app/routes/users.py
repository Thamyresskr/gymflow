
"""
Rotas de gerenciamento de usuários.

Responsabilidades:
- Receber requisições relacionadas aos usuários.
- Delegar as regras de negócio para a camada de serviços.
- Disponibilizar operações de cadastro, consulta, atualização
  e remoção de usuários.
- Restringir operações administrativas ao perfil ADMIN.
- Permitir à RECEPCAO cadastrar exclusivamente alunos.
"""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, require_roles
from app.core.dependencies import get_db
from app.models.user import User
from app.schemas.error import ErrorResponse
from app.schemas.user import (
    AdminUserCreate,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import (
    get_user,
    list_users,
    register_admin_user,
    register_user,
    remove_user,
    update_user_data,
)

router = APIRouter(
    prefix="/users",
    tags=["Usuários"],
)


# ==========================================================
# Cadastro público de alunos
# ==========================================================

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar aluno",
    response_description="Aluno cadastrado com sucesso.",
    description="""
Realiza o cadastro público de um novo aluno.

O perfil inicial é ALUNO e não pode ser escolhido
pelo solicitante. Esta rota não requer autenticação.
""",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Dados inválidos.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "E-mail ou matrícula já cadastrados.",
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
    """Cadastra um aluno pelo fluxo público."""
    return register_user(
        db=db,
        user_data=usuario,
    )


# ==========================================================
# Cadastro de alunos pela RECEPÇÃO
# ==========================================================

@router.post(
    "/reception",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar aluno pela recepção",
    response_description="Aluno cadastrado com sucesso.",
    description="""
Permite que um usuário autenticado com perfil RECEPCAO
cadastre exclusivamente alunos.

O perfil não pode ser escolhido pelo solicitante.
""",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Apenas RECEPCAO pode utilizar esta rota.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "E-mail ou matrícula já cadastrados.",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "model": ErrorResponse,
            "description": "Erro de validação.",
        },
    },
)
def criar_aluno_recepcao(
    usuario: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("RECEPCAO")),
) -> UserResponse:
    """Cadastra um aluno utilizando as regras existentes."""
    return register_user(
        db=db,
        user_data=usuario,
    )


# ==========================================================
# Cadastro administrativo
# ==========================================================

@router.post(
    "/admin",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar usuário por perfil",
    response_description="Usuário criado pelo administrador.",
    description="""
Cria um usuário com o perfil especificado.

Requer autenticação e o perfil ADMIN.
A criação de outro ADMIN é bloqueada pelo schema e pelo serviço.
""",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Apenas ADMIN pode criar usuários por perfil.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "E-mail ou matrícula já cadastrados.",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "model": ErrorResponse,
            "description": "Dados inválidos.",
        },
    },
)
def criar_usuario_administrativo(
    usuario: AdminUserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> UserResponse:
    """Cria um usuário com o perfil selecionado pelo ADMIN."""
    return register_admin_user(
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
    """Retorna todos os usuários cadastrados. Requer ADMIN."""
    return list_users(db=db)


# ==========================================================
# Dados do próprio usuário
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obter usuário autenticado",
    response_description="Dados do usuário autenticado.",
    description="Retorna os dados do usuário associado ao token JWT.",
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
    """Retorna os dados do usuário autenticado."""
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
    """Busca um usuário pelo identificador. Requer ADMIN."""
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
            "description": "E-mail ou matrícula já cadastrados.",
        },
    },
)
def atualizar_usuario(
    user_id: int,
    usuario: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
) -> UserResponse:
    """Atualiza os dados de um usuário. Requer ADMIN."""
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
    """Remove um usuário. Requer ADMIN."""
    remove_user(
        db=db,
        user_id=user_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
