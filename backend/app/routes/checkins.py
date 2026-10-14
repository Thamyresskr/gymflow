
"""
Rotas relacionadas ao gerenciamento de check-ins.

Responsabilidades:
- Receber as requisições relacionadas aos check-ins.
- Validar os dados de entrada.
- Delegar as regras de negócio para a camada de serviços.
- Retornar as informações dos check-ins solicitados.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, require_roles
from app.core.dependencies import get_db
from app.crud.checkin import (
    get_active_checkins,
    get_all_checkins,
    get_user_checkins,
)
from app.models.user import User
from app.schemas.checkin import CheckinResponse
from app.schemas.error import ErrorResponse
from app.services.checkin_service import (
    finish_checkin,
    register_checkin,
)

router = APIRouter(
    prefix="/checkins",
    tags=["Check-ins"],
)


@router.post(
    "/",
    response_model=CheckinResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Realizar check-in",
    description="""
Registra a entrada do usuário autenticado na academia.

Regras de negócio:
- O usuário deve estar autenticado.
- O check-in é associado ao usuário autenticado.
- Não pode existir outro check-in ativo para o mesmo usuário.
""",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "O usuário já possui um check-in ativo.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "model": ErrorResponse,
            "description": "Erro de validação dos dados enviados.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor.",
        },
    },
)
def realizar_checkin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CheckinResponse:
    """Registra o check-in do usuário autenticado."""

    return register_checkin(
        db=db,
        current_user=current_user,
    )


@router.put(
    "/{checkin_id}/checkout",
    response_model=CheckinResponse,
    status_code=status.HTTP_200_OK,
    summary="Realizar check-out",
    description="""
Finaliza um check-in em aberto.

Regras de negócio:
- O usuário deve estar autenticado.
- O check-in deve existir e estar ativo.
- ALUNO e PROFESSOR só podem finalizar o próprio check-in.
- ADMIN e RECEPCAO podem finalizar check-ins de outros usuários.
""",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Você não possui permissão para finalizar este check-in.",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Check-in não encontrado.",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "model": ErrorResponse,
            "description": "Erro de validação dos dados enviados.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor.",
        },
    },
)
def realizar_checkout(
    checkin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CheckinResponse:
    """Finaliza um check-in conforme as permissões do usuário."""

    return finish_checkin(
        db=db,
        checkin_id=checkin_id,
        current_user=current_user,
    )


@router.get(
    "/ativos",
    response_model=list[CheckinResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar check-ins ativos",
    description="""
Retorna todos os check-ins que ainda não possuem horário de saída.

Acesso permitido apenas aos perfis ADMIN e RECEPCAO.
""",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Acesso permitido apenas para ADMIN e RECEPCAO.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor.",
        },
    },
)
def listar_checkins_ativos(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN", "RECEPCAO")),
) -> list[CheckinResponse]:
    """Retorna todos os check-ins ativos."""

    return get_active_checkins(db=db)


@router.get(
    "/me",
    response_model=list[CheckinResponse],
    status_code=status.HTTP_200_OK,
    summary="Histórico do usuário autenticado",
    description="""
Retorna apenas os check-ins pertencentes ao usuário autenticado.
O identificador do usuário é obtido pelo token JWT.
""",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor.",
        },
    },
)
def listar_meus_checkins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CheckinResponse]:
    """Retorna o histórico de check-ins do usuário autenticado."""

    return get_user_checkins(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/",
    response_model=list[CheckinResponse],
    status_code=status.HTTP_200_OK,
    summary="Histórico completo de check-ins",
    description="""
Retorna o histórico completo de check-ins da aplicação.

Acesso permitido apenas aos perfis ADMIN e RECEPCAO.
""",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Acesso permitido apenas para ADMIN e RECEPCAO.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor.",
        },
    },
)
def listar_checkins(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN", "RECEPCAO")),
) -> list[CheckinResponse]:
    """Retorna o histórico completo de check-ins."""

    return get_all_checkins(db=db)
