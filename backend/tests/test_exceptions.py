"""
Testes das exceções personalizadas da aplicação.
"""

from fastapi import status

from app.core.exceptions import (
    AppException,
    CheckinAlreadyOpenException,
    CheckinNotFoundException,
    InvalidCredentialsException,
    InvalidTokenException,
    UnauthorizedException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


def test_app_exception_base():
    """
    Deve criar uma exceção base corretamente.
    """

    exception = AppException(
        message="Erro de teste.",
        code="TEST_ERROR",
    )

    assert exception.message == "Erro de teste."
    assert exception.code == "TEST_ERROR"
    assert exception.status_code == status.HTTP_400_BAD_REQUEST


def test_user_not_found_exception():
    """
    Deve criar exceção de usuário inexistente.
    """

    exception = UserNotFoundException()

    assert exception.message == "Usuário não encontrado."
    assert exception.code == "USER_NOT_FOUND"
    assert exception.status_code == status.HTTP_404_NOT_FOUND


def test_user_already_exists_exception():
    """
    Deve criar exceção de usuário duplicado.
    """

    exception = UserAlreadyExistsException()

    assert exception.code == "USER_ALREADY_EXISTS"
    assert exception.status_code == status.HTTP_409_CONFLICT


def test_invalid_credentials_exception():
    """
    Deve criar exceção de credenciais inválidas.
    """

    exception = InvalidCredentialsException()

    assert exception.code == "INVALID_CREDENTIALS"
    assert exception.status_code == status.HTTP_401_UNAUTHORIZED


def test_invalid_token_exception():
    """
    Deve criar exceção de token inválido.
    """

    exception = InvalidTokenException()

    assert exception.code == "INVALID_TOKEN"
    assert exception.status_code == status.HTTP_401_UNAUTHORIZED


def test_checkin_already_open_exception():
    """
    Deve criar exceção de check-in aberto.
    """

    exception = CheckinAlreadyOpenException()

    assert exception.code == "CHECKIN_ALREADY_OPEN"
    assert exception.status_code == status.HTTP_409_CONFLICT


def test_checkin_not_found_exception():
    """
    Deve criar exceção de check-in inexistente.
    """

    exception = CheckinNotFoundException()

    assert exception.code == "CHECKIN_NOT_FOUND"
    assert exception.status_code == status.HTTP_404_NOT_FOUND


def test_unauthorized_exception():
    """
    Deve criar exceção de permissão negada.
    """

    exception = UnauthorizedException()

    assert exception.code == "UNAUTHORIZED"
    assert exception.status_code == status.HTTP_403_FORBIDDEN