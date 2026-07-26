"""
Serviços relacionados ao Dashboard.

Responsabilidades:
- Consolidar os indicadores do Dashboard.
- Orquestrar consultas da camada CRUD.
- Montar os objetos de resposta da API.
"""

from sqlalchemy.orm import Session

from app.crud.dashboard import (
    get_checkins_hoje,
    get_checkouts_hoje,
    get_ocupacao_atual,
    get_tempo_medio_permanencia,
    get_ultimos_checkins,
)
from app.schemas.dashboard import (
    DashboardResponse,
    DashboardResumo,
    DashboardUltimoCheckin,
)


def get_dashboard(
    db: Session,
) -> DashboardResponse:
    """
    Obtém os indicadores consolidados do Dashboard.

    Reúne as principais métricas da aplicação, incluindo ocupação
    atual, quantidade de check-ins e check-outs realizados no dia,
    tempo médio de permanência e a lista dos últimos check-ins.

    Args:
        db: Sessão ativa do banco de dados.

    Returns:
        DashboardResponse: Objeto contendo o resumo dos indicadores
        e os últimos check-ins registrados.
    """

    resumo = DashboardResumo(
        ocupacao_atual=get_ocupacao_atual(db=db),
        checkins_hoje=get_checkins_hoje(db=db),
        checkouts_hoje=get_checkouts_hoje(db=db),
        tempo_medio_permanencia=get_tempo_medio_permanencia(db=db),
    )

    ultimos_checkins = [
        DashboardUltimoCheckin(
            usuario=usuario.nome,
            entrada=checkin.checkin_time,
            saida=checkin.checkout_time,
        )
        for checkin, usuario in get_ultimos_checkins(db=db)
    ]

    return DashboardResponse(
        resumo=resumo,
        ultimos_checkins=ultimos_checkins,
    )