"""
Camada de acesso a dados (CRUD) para check-ins.

Responsabilidades:
- Persistir check-ins.
- Consultar check-ins.
- Atualizar check-ins.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.checkin import Checkin


def create_checkin(
    db: Session,
    checkin: Checkin,
) -> Checkin:
    """
    Persiste um novo check-in.

    Args:
        db: Sessão ativa do banco de dados.
        checkin: Instância do check-in a ser persistida.

    Returns:
        Checkin: Check-in criado.
    """

    db.add(checkin)
    db.commit()
    db.refresh(checkin)

    return checkin


def get_open_checkin(
    db: Session,
    user_id: int,
) -> Checkin | None:
    """
    Retorna o check-in em aberto de um usuário.

    Args:
        db: Sessão ativa do banco de dados.
        user_id: Identificador do usuário.

    Returns:
        Checkin | None: Check-in ativo ou ``None`` caso não exista.
    """

    return (
        db.query(Checkin)
        .filter(
            Checkin.user_id == user_id,
            Checkin.checkout_time.is_(None),
        )
        .first()
    )


def get_checkin_by_id(
    db: Session,
    checkin_id: int,
) -> Checkin | None:
    """
    Busca um check-in pelo identificador.

    Args:
        db: Sessão ativa do banco de dados.
        checkin_id: Identificador do check-in.

    Returns:
        Checkin | None: Check-in encontrado ou ``None``.
    """

    return (
        db.query(Checkin)
        .filter(Checkin.id == checkin_id)
        .first()
    )


def get_all_checkins(
    db: Session,
) -> list[Checkin]:
    """
    Retorna o histórico completo de check-ins.

    Os registros são ordenados do mais recente para o mais antigo.

    Args:
        db: Sessão ativa do banco de dados.

    Returns:
        list[Checkin]: Lista de check-ins.
    """

    return (
        db.query(Checkin)
        .order_by(Checkin.checkin_time.desc())
        .all()
    )


def get_active_checkins(
    db: Session,
) -> list[Checkin]:
    """
    Retorna todos os check-ins ativos.

    Args:
        db: Sessão ativa do banco de dados.

    Returns:
        list[Checkin]: Lista de check-ins sem horário de check-out.
    """

    return (
        db.query(Checkin)
        .filter(Checkin.checkout_time.is_(None))
        .order_by(Checkin.checkin_time.desc())
        .all()
    )


def update_checkin(
    db: Session,
    checkin: Checkin,
) -> Checkin:
    """
    Persiste alterações realizadas em um check-in.

    Args:
        db: Sessão ativa do banco de dados.
        checkin: Instância do check-in com as alterações.

    Returns:
        Checkin: Check-in atualizado.
    """

    db.commit()
    db.refresh(checkin)

    return checkin


def checkout(
    db: Session,
    checkin: Checkin,
) -> Checkin:
    """
    Finaliza um check-in registrando o horário de saída.

    Define o horário de check-out utilizando UTC e persiste
    a alteração no banco de dados.

    Args:
        db: Sessão ativa do banco de dados.
        checkin: Check-in a ser finalizado.

    Returns:
        Checkin: Check-in atualizado.
    """

    checkin.checkout_time = datetime.now(timezone.utc)

    return update_checkin(
        db=db,
        checkin=checkin,
    )