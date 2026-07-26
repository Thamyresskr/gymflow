"""
Exceções personalizadas da aplicação.
"""

from fastapi import status


class AppException(Exception):
    """
    Exceção base da aplicação.
    """

    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class UserNotFoundException(AppException):
    """
    Usuário não encontrado.
    """

    def __init__(self):
        super().__init__(
            message="Usuário não encontrado.",
            code="USER_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UserAlreadyExistsException(AppException):
    """
    Usuário já cadastrado.
    """

    def __init__(self):
        super().__init__(
            message="Já existe um usuário com este e-mail.",
            code="USER_ALREADY_EXISTS",
            status_code=status.HTTP_409_CONFLICT,
        )


class InvalidCredentialsException(AppException):
    """
    Credenciais inválidas.
    """

    def __init__(self):
        super().__init__(
            message="E-mail ou senha inválidos.",
            code="INVALID_CREDENTIALS",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class InvalidTokenException(AppException):
    """
    Token inválido ou expirado.
    """

    def __init__(self):
        super().__init__(
            message="Token inválido ou expirado.",
            code="INVALID_TOKEN",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class CheckinAlreadyOpenException(AppException):
    """
    Usuário já possui um check-in ativo.
    """

    def __init__(self):
        super().__init__(
            message="O usuário já possui um check-in ativo.",
            code="CHECKIN_ALREADY_OPEN",
            status_code=status.HTTP_409_CONFLICT,
        )


class CheckinNotFoundException(AppException):
    """
    Check-in não encontrado.
    """

    def __init__(self):
        super().__init__(
            message="Check-in não encontrado.",
            code="CHECKIN_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UnauthorizedException(AppException):
    """
    Acesso não autorizado.
    """

    def __init__(self):
        super().__init__(
            message="Você não possui permissão para executar esta ação.",
            code="UNAUTHORIZED",
            status_code=status.HTTP_403_FORBIDDEN,
        )