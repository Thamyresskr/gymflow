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
    summary="Dashboard gerencial",
    description="""
Retorna os principais indicadores da academia.

### Informações retornadas

- Quantidade de usuários cadastrados
- Quantidade de check-ins ativos
- Quantidade total de check-ins
- Demais indicadores definidos pela aplicação

### Requisitos

É necessário estar autenticado utilizando um JWT válido.
""",
    responses={
        200: {
            "description": "Indicadores retornados com sucesso."
        },
        401: {
            "description": "Usuário não autenticado."
        },
    },
)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardResponse:
    """
    Retorna os indicadores consolidados da academia.

    Requer autenticação via JWT.
    """

    return get_dashboard(db=db)