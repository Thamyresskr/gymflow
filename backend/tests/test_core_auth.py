"""
Testes do módulo app.core.auth.
"""

import pytest
from fastapi import HTTPException, status

from app.core.auth import get_current_user


def test_get_current_user_token_sem_id(monkeypatch):
    """
    Deve retornar 401 quando o token não possuir o campo 'id'.
    """

    from app.core import auth

    monkeypatch.setattr(
        auth,
        "decode_access_token",
        lambda token: {},
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(
            token="token_fake",
            db=None,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Token inválido."


def test_get_current_user_usuario_nao_encontrado(monkeypatch):
    """
    Deve retornar 401 quando o usuário não existir.
    """

    from app.core import auth

    monkeypatch.setattr(
        auth,
        "decode_access_token",
        lambda token: {"id": 999},
    )

    monkeypatch.setattr(
        auth,
        "get_user_by_id",
        lambda db, user_id: None,
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(
            token="token_fake",
            db=None,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Usuário não encontrado."