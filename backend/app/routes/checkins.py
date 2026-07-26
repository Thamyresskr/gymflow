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

from app.core.auth import get_current_user
from app.core.dependencies import get_db
from app.crud.checkin import (
    get_active_checkins,
    get_all_checkins,
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
- Não pode existir outro check-in ativo para o mesmo usuário.

Retorna o registro do check-in criado.
""",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Check-in realizado com sucesso.",
        },
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
    """
    Registra o check-in do usuário autenticado.

    Encaminha a solicitação para a camada de serviços, responsável
    por validar as regras de negócio e registrar a entrada do usuário.

    Args:
        db: Sessão ativa do banco de dados.
        current_user: Usuário autenticado.

    Returns:
        CheckinResponse: Dados do check-in criado.
    """

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
- O check-in informado deve existir.
- O check-in deve estar ativo.

Retorna o registro atualizado do check-in.
""",
    responses={
        status.HTTP_200_OK: {
            "description": "Check-out realizado com sucesso.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Usuário não autenticado.",
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
    """
    Finaliza um check-in ativo.

    Encaminha a solicitação para a camada de serviços, responsável
    por localizar o check-in, validar seu estado e registrar o horário
    de saída.

    Args:
        checkin_id: Identificador do check-in.
        db: Sessão ativa do banco de dados.
        current_user: Usuário autenticado.

    Returns:
        CheckinResponse: Dados atualizados do check-in.
    """

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

Este endpoint requer autenticação utilizando um token JWT válido.
""",
    responses={
        status.HTTP_200_OK: {
            "description": "Lista de check-ins ativos retornada com sucesso.",
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
def listar_checkins_ativos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CheckinResponse]:
    """
    Retorna todos os check-ins ativos.

    Args:
        db: Sessão ativa do banco de dados.
        current_user: Usuário autenticado.

    Returns:
        list[CheckinResponse]: Lista de check-ins ativos.
    """

    return get_active_checkins(db=db)


@router.get(
    "/",
    response_model=list[CheckinResponse],
    status_code=status.HTTP_200_OK,
    summary="Histórico de check-ins",
    description="""
Retorna o histórico completo de check-ins registrados na aplicação.

Este endpoint requer autenticação utilizando um token JWT válido.
""",
    responses={
        status.HTTP_200_OK: {
            "description": "Histórico retornado com sucesso.",
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
def listar_checkins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CheckinResponse]:
    """
    Retorna o histórico completo de check-ins.

    Args:
        db: Sessão ativa do banco de dados.
        current_user: Usuário autenticado.

    Returns:
        list[CheckinResponse]: Histórico de check-ins registrados.
    """

    return get_all_checkins(db=db)