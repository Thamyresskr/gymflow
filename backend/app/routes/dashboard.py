"""
Rotas relacionadas ao Dashboard.

Responsabilidades:
- Receber as requisições relacionadas ao Dashboard.
- Validar o acesso do usuário autenticado.
- Delegar a geração dos indicadores para a camada de serviços.
- Retornar os dados consolidados da aplicação.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
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

As informações apresentadas são consolidadas em tempo real e
podem incluir:

- Ocupação atual da academia.
- Quantidade de check-ins realizados no dia.
- Quantidade de check-outs realizados no dia.
- Tempo médio de permanência dos usuários.
- Relação dos últimos check-ins registrados.

Este endpoint requer autenticação utilizando um token JWT válido.
""",
    responses={
        status.HTTP_200_OK: {
            "description": "Indicadores retornados com sucesso.",
        },
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
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardResponse:
    """
    Retorna os indicadores consolidados da academia.

    Após validar a autenticação do usuário, a solicitação é
    encaminhada para a camada de serviços, responsável por
    consolidar os indicadores exibidos no Dashboard.

    Args:
        db: Sessão ativa do banco de dados.
        current_user: Usuário autenticado.

    Returns:
        DashboardResponse: Indicadores consolidados da aplicação.
    """

    return get_dashboard(db=db)