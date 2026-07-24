"""
Rotas relacionadas aos check-ins.

Responsabilidades:
- Receber requisições HTTP
- Delegar regras de negócio para a camada Service
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.dependencies import get_db
from app.crud.checkin import (
    get_active_checkins,
    get_all_checkins,
)
from app.models.user import User
from app.schemas.checkin import CheckinResponse
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
    description="Registra a entrada do usuário autenticado na academia.",
)
def realizar_checkin(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CheckinResponse:
    """
    Realiza o check-in do usuário autenticado.
    """

    return register_checkin(
        db=db,
        current_user=current_user,
    )


@router.put(
    "/{checkin_id}/checkout",
    response_model=CheckinResponse,
    summary="Realizar checkout",
    description="Finaliza um check-in em aberto.",
)
def realizar_checkout(
    checkin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CheckinResponse:
    """
    Finaliza um check-in.
    """

    return finish_checkin(
        db=db,
        checkin_id=checkin_id,
        current_user=current_user,
    )


@router.get(
    "/ativos",
    response_model=list[CheckinResponse],
    summary="Listar check-ins ativos",
)
def listar_checkins_ativos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CheckinResponse]:
    """
    Lista todos os check-ins ativos.
    """

    return get_active_checkins(db=db)


@router.get(
    "/",
    response_model=list[CheckinResponse],
    summary="Histórico de check-ins",
)
def listar_checkins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CheckinResponse]:
    """
    Retorna o histórico completo de check-ins.
    """

    return get_all_checkins(db=db)