
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
    create_admin_user,
    create_user,
    delete_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    get_user_by_matricula,
    update_user,
)
from app.models.user import TipoUsuario, User
from app.schemas.user import (
    AdminUserCreate,
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


def _validate_unique_user_data(
    db: Session,
    *,
    email: str,
    matricula: str | None,
) -> None:
    """
    Valida a unicidade do e-mail e, quando informada,
    da matrícula.
    """
    usuario_existente = get_user_by_email(
        db=db,
        email=email,
    )

    if usuario_existente is not None:
        logger.warning(
            "Tentativa de cadastro com email ja existente | email=%s",
            email,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado.",
        )

    if matricula is not None:
        matricula_existente = get_user_by_matricula(
            db=db,
            matricula=matricula,
        )

        if matricula_existente is not None:
            logger.warning(
                "Tentativa de cadastro com matricula existente."
            )

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Matrícula já cadastrada.",
            )


def register_user(
    db: Session,
    user_data: UserCreate,
) -> UserResponse:
    """
    Cadastra um usuário público com perfil ALUNO.
    """
    _validate_unique_user_data(
        db=db,
        email=user_data.email,
        matricula=user_data.matricula,
    )

    try:
        usuario = create_user(
            db=db,
            user_data=user_data,
        )

    except IntegrityError as exc:
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


def register_admin_user(
    db: Session,
    user_data: AdminUserCreate,
) -> UserResponse:
    """
    Cadastra um usuário com o perfil definido pelo ADMIN.

    A autorização deve ser verificada pela rota antes
    de chamar este serviço.
    """
    # Proteção adicional: impede criar outro ADMIN
    # mesmo se a validação do schema for contornada.
    if user_data.tipo == TipoUsuario.ADMIN:
        logger.warning(
            "Tentativa de criar usuario ADMIN pela rota administrativa."
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não é permitido criar usuários ADMIN por esta rota.",
        )

    _validate_unique_user_data(
        db=db,
        email=user_data.email,
        matricula=user_data.matricula,
    )

    try:
        usuario = create_admin_user(
            db=db,
            user_data=user_data,
        )

    except IntegrityError as exc:
        logger.warning(
            "Violacao de integridade no cadastro administrativo."
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "E-mail ou matrícula já cadastrados. "
                "Verifique os dados informados."
            ),
        ) from exc

    logger.info(
        "Usuario criado administrativamente | id=%s | perfil=%s",
        usuario.id,
        usuario.tipo.value,
    )

    return usuario


def list_users(
    db: Session,
) -> list[User]:
    """
    Retorna todos os usuários cadastrados.
    """
    return get_all_users(db=db)


def get_user(
    db: Session,
    user_id: int,
) -> User:
    """
    Retorna um usuário pelo identificador.
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
    O perfil não é alterado por este serviço.
    """
    usuario = _get_existing_user(
        db=db,
        user_id=user_id,
    )

    dados = user_data.model_dump(exclude_unset=True)

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
        setattr(usuario, campo, valor)

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
