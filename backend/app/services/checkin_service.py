"""
Regras de negócio relacionadas aos check-ins.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.crud.checkin import (
    checkout,
    create_checkin,
    get_checkin_by_id,
    get_open_checkin,
)
from app.models.checkin import Checkin
from app.models.user import User


def register_checkin(
    db: Session,
    current_user: User,
) -> Checkin:
    """
    Realiza o check-in do usuário.

    Args:
        db: Sessão do banco de dados.
        current_user: Usuário autenticado.

    Returns:
        Check-in criado.

    Raises:
        HTTPException: Caso o usuário já possua um check-in em aberto.
    """

    checkin_aberto = get_open_checkin(
        db=db,
        user_id=current_user.id,
    )

    if checkin_aberto:
        logger.warning(
            "Tentativa de novo check-in com outro em aberto | usuário=%s | id=%s",
            current_user.email,
            current_user.id,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O usuário já possui um check-in em aberto.",
        )

    checkin = create_checkin(
        db=db,
        checkin=Checkin(
            user_id=current_user.id,
        ),
    )

    logger.info(
        "Check-in realizado | usuário=%s | id=%s | checkin=%s",
        current_user.email,
        current_user.id,
        checkin.id,
    )

    return checkin


def finish_checkin(
    db: Session,
    checkin_id: int,
    current_user: User,
) -> Checkin:
    """
    Finaliza um check-in.

    Args:
        db: Sessão do banco de dados.
        checkin_id: Identificador do check-in.
        current_user: Usuário autenticado.

    Returns:
        Check-in finalizado.

    Raises:
        HTTPException:
            - Caso o check-in não exista;
            - Caso pertença a outro usuário;
            - Caso já tenha sido finalizado.
    """

    checkin = get_checkin_by_id(
        db=db,
        checkin_id=checkin_id,
    )

    if checkin is None:
        logger.warning(
            "Tentativa de finalizar check-in inexistente | checkin=%s",
            checkin_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Check-in não encontrado.",
        )

    if checkin.user_id != current_user.id:
        logger.warning(
            "Tentativa de finalizar check-in de outro usuário | usuário=%s | checkin=%s",
            current_user.email,
            checkin.id,
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não possui permissão para finalizar este check-in.",
        )

    if checkin.checkout_time is not None:
        logger.warning(
            "Tentativa de finalizar check-in já encerrado | usuário=%s | checkin=%s",
            current_user.email,
            checkin.id,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este check-in já foi finalizado.",
        )

    checkin = checkout(
        db=db,
        checkin=checkin,
    )

    logger.info(
        "Checkout realizado | usuário=%s | id=%s | checkin=%s",
        current_user.email,
        current_user.id,
        checkin.id,
    )

    return checkin