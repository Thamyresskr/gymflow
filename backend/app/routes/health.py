"""
Rotas de monitoramento da API.
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=HealthResponse,
    summary="Verificar saúde da API",
    description="""
Retorna o status atual da API.

Este endpoint pode ser utilizado por ferramentas de monitoramento
para verificar se a aplicação está disponível.
""",
)
async def health_check():
    """
    Endpoint de Health Check.
    """

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now(timezone.utc),
    )