"""
Centraliza as configurações da aplicação GymFlow.

Todas as configurações podem ser sobrescritas por variáveis
de ambiente, facilitando a execução em diferentes ambientes.
"""

import os


class Settings:
    """Configurações gerais da aplicação."""

    # =========================================================================
    # API
    # =========================================================================

    APP_NAME: str = os.getenv(
        "APP_NAME",
        "GymFlow API",
    )

    VERSION: str = os.getenv(
        "VERSION",
        "1.0.0",
    )

    # =========================================================================
    # Banco de dados
    # =========================================================================

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./gymflow.db",
    )

    # =========================================================================
    # Segurança
    # =========================================================================

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "troque-esta-chave-em-seu-arquivo-env",
    )

    ALGORITHM: str = os.getenv(
        "ALGORITHM",
        "HS256",
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            60,
        )
    )


settings = Settings()