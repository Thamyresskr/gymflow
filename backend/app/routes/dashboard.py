
"""
Rotas relacionadas ao Dashboard.

Responsabilidades:
- Validar o acesso do usuário autenticado.
- Restringir o Dashboard aos perfis autorizados.
- Delegar a geração dos indicadores para a camada de serviços.
- Retornar os dados consolidados da aplicação.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import require_roles
from app.core.dependencies import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.schemas.error import ErrorResponse
from app.services.dashboard_service import get_dashboard

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/",
    response_model=DashboardResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar Dashboard",
    description="""
Retorna os principais indicadores da academia.

Permissões:
- ADMIN: acesso aos indicadores gerais.
- RECEPCAO: acesso aos indicadores gerais.

Indicadores disponibilizados:
- Ocupação atual da academia.
- Quantidade de check-ins realizados no dia.
- Quantidade de check-outs realizados no dia.
- Tempo médio de permanência dos usuários.
- Relação dos últimos check-ins registrados.
""",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description=": "Acesso permitido apenas para ADMIN e RECEPCAO.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor.",
        },
    },
)
def dashboard(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("ADMIN", "RECEPCAO")),
) -> DashboardResponse:
    """Retorna os indicadores consolidados da academia."""

    return get_dashboard(db=db)
