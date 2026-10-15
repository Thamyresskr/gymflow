"""
Rotas relacionadas ao Dashboard.

Permissões:
- ADMIN, RECEPCAO e PROFESSOR: acesso aos indicadores completos.
- Todos os perfis autenticados: acesso à ocupação atual.
- ALUNO: não pode consultar o dashboard completo.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, require_roles
from app.core.dependencies import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.schemas.error import ErrorResponse
from app.services.dashboard_service import (
    get_dashboard,
    get_resumo_ocupacao,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/ocupacao",
    status_code=status.HTTP_200_OK,
    summary="Consultar ocupação atual",
    description=(
        "Retorna somente a quantidade de pessoas presentes "
        "na academia, sem expor dados pessoais. "
        "Disponível para todos os perfis autenticados."
    ),
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
def consultar_ocupacao(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, int]:
    """Retorna apenas a ocupação atual da academia."""

    return get_resumo_ocupacao(db=db)


@router.get(
    "/",
    response_model=DashboardResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar dashboard completo",
    description=(
        "Retorna indicadores gerais e últimos check-ins. "
        "Permitido para ADMIN, RECEPCAO e PROFESSOR."
    ),
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": (
                "Acesso permitido somente para ADMIN, "
                "RECEPCAO e PROFESSOR."
            ),
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor.",
        },
    },
)
def dashboard(
    db: Session = Depends(get_db),
    _: User = Depends(
        require_roles("ADMIN", "RECEPCAO", "PROFESSOR")
    ),
) -> DashboardResponse:
    """Retorna os indicadores completos da academia."""

    return get_dashboard(db=db)
