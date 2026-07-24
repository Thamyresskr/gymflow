"""
Rotas do Dashboard.

Responsabilidades:
- Receber requisições HTTP
- Delegar regras de negócio para a camada Service
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.dependencies import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import get_dashboard

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/",
    response_model=DashboardResponse,
    summary="Dashboard",
    description="Retorna os indicadores principais da academia.",
)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardResponse:
    """
    Retorna os indicadores principais do Dashboard.
    """

    return get_dashboard(db=db)