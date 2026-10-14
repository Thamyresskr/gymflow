"""
Serviços relacionados ao gerenciamento de usuários.

Responsabilidades:
- Validar regras de negócio relacionadas aos usuários.
- Garantir integridade dos dados.
- Delegar a persistência para a camada CRUD.
- Registrar eventos relevantes da aplicação.
"""

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.crud.user import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    get_user_by_matricula,
    update_user,
)
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)


def _get_existing_user(
    db: Session,
    user_id: int,
) -> User:
    """
    Recupera um usuário existente.

    Args:
        db: Sessão ativa do banco.
        user_id: Identificador do usuário.

    Returns:
        User: Usuário encontrado.

    Raises:
        HTTPException: Caso o usuário não exista.
    """
    usuario = get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if usuario is None:
        logger.warning(
            "Usuario nao encontrado | id=%s",
            user_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    return usuario


def register_user(
    db: Session,
    user_data: UserCreate,
) -> UserResponse:
    """
    Realiza o cadastro de um novo usuário.

    Args:
        db: Sessão ativa do banco.
        user_data: Dados do usuário.

    Returns:
        UserResponse: Usuário cadastrado.

    Raises:
        HTTPException: Caso o e-mail ou a matrícula já estejam
            cadastrados.
    """
    usuario_existente = get_user_by_email(
        db=db,
        email=user_data.email,
    )

    if usuario_existente is not None:
        logger.warning(
            "Tentativa de cadastro com email ja existente | email=%s",
            user_data.email,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado.",
        )

    # Matrícula é opcional; só verificar duplicidade quando informada.
    if user_data.matricula is not None:
        matricula_existente = get_user_by_matricula(
            db=db,
            matricula=user_data.matricula,
        )

        if matricula_existente is not None:
            logger.warning(
                "Tentativa de cadastro com matricula existente."
            )

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Matrícula já cadastrada.",
            )

    try:
        usuario = create_user(
            db=db,
            user_data=user_data,
        )

    except IntegrityError as exc:
        # O CRUD executa rollback antes de relançar o erro.
        logger.warning(
            "Violacao de integridade durante cadastro de usuario."
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "E-mail ou matrícula já cadastrados. "
                "Verifique os dados informados."
            ),
        ) from exc

    logger.info(
        "Usuario cadastrado | id=%s | email=%s",
        usuario.id,
        usuario.email,
    )

    return usuario


def list_users(
    db: Session,
) -> list[User]:
    """
    Retorna todos os usuários cadastrados.

    Args:
        db: Sessão ativa do banco.

    Returns:
        list[User]: Lista de usuários cadastrados.
    """
    return get_all_users(db=db)


def get_user(
    db: Session,
    user_id: int,
) -> User:
    """
    Retorna um usuário pelo identificador.

    Args:
        db: Sessão ativa do banco.
        user_id: Identificador do usuário.

    Returns:
        User: Usuário encontrado.

    Raises:
        HTTPException: Caso o usuário não exista.
    """
    return _get_existing_user(
        db=db,
        user_id=user_id,
    )


def update_user_data(
    db: Session,
    user_id: int,
    user_data: UserUpdate,
) -> User:
    """
    Atualiza parcialmente os dados de um usuário.

    Apenas os campos enviados serão alterados.

    Args:
        db: Sessão ativa do banco.
        user_id: Identificador do usuário.
        user_data: Dados que serão atualizados.

    Returns:
        User: Usuário atualizado.

    Raises:
        HTTPException: Caso o usuário não exista ou os dados
            violem uma restrição de unicidade ou integridade.
    """
    usuario = _get_existing_user(
        db=db,
        user_id=user_id,
    )

    dados = user_data.model_dump(exclude_unset=True)

    # Verifica e-mail somente se ele estiver sendo atualizado.
    if "email" in dados:
        usuario_existente = get_user_by_email(
            db=db,
            email=dados["email"],
        )

        if (
            usuario_existente is not None
            and usuario_existente.id != usuario.id
        ):
            logger.warning(
                "Tentativa de atualizar para email ja existente | email=%s",
                dados["email"],
            )

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado.",
            )

    # A matrícula pode ser nula; verificar apenas quando preenchida.
    if "matricula" in dados and dados["matricula"] is not None:
        matricula_existente = get_user_by_matricula(
            db=db,
            matricula=dados["matricula"],
        )

        if (
            matricula_existente is not None
            and matricula_existente.id != usuario.id
        ):
            logger.warning(
                "Tentativa de atualizar para matricula existente."
            )

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Matrícula já cadastrada.",
            )

    for campo, valor in dados.items():
        setattr(
            usuario,
            campo,
            valor,
        )

    try:
        usuario = update_user(
            db=db,
            user=usuario,
        )

    except IntegrityError as exc:
        logger.warning(
            "Violacao de integridade ao atualizar usuario | id=%s",
            user_id,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Os dados informados violam uma restrição "
                "de integridade ou unicidade."
            ),
        ) from exc

    logger.info(
        "Usuario atualizado | id=%s",
        usuario.id,
    )

    return usuario


def remove_user(
    db: Session,
    user_id: int,
) -> None:
    """
    Remove um usuário.

    Args:
        db: Sessão ativa do banco.
        user_id: Identificador do usuário.

    Raises:
        HTTPException: Caso o usuário não exista ou a exclusão
            viole uma restrição de integridade.
    """
    usuario = _get_existing_user(
        db=db,
        user_id=user_id,
    )

    try:
        delete_user(
            db=db,
            user=usuario,
        )

    except IntegrityError as exc:
        logger.warning(
            "Violacao de integridade ao remover usuario | id=%s",
            user_id,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Não foi possível remover o usuário "
                "devido a uma restrição de integridade."
            ),
        ) from exc

    logger.info(
        "Usuario removido | id=%s",
        user_id,
    )
