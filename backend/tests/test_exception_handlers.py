"""
Testes dos handlers globais de exceções.
"""

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app


def test_http_exception_handler(client):
    """
    Deve retornar o padrão da API para exceções HTTP.
    """

    @app.get("/__teste404")
    def rota_http():
        raise HTTPException(
            status_code=404,
            detail="Recurso não encontrado.",
        )

    response = client.get("/__teste404")

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == 404
    assert data["message"] == "Recurso não encontrado."
    assert data["path"] == "/__teste404"
    assert "timestamp" in data


def test_validation_exception_handler(client):
    """
    Deve retornar o padrão da API para erros de validação.
    """

    response = client.post(
        "/users/",
        json={},
    )

    assert response.status_code == 422

    data = response.json()

    assert data["status"] == 422
    assert data["message"] == "Dados da requisição inválidos."
    assert data["path"] == "/users/"
    assert "timestamp" in data
    assert "errors" in data


def test_global_exception_handler():
    """
    Deve retornar erro 500 para exceções inesperadas.
    """

    @app.get("/__teste500")
    def rota_erro():
        raise RuntimeError("Erro proposital")

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/__teste500")

    assert response.status_code == 500

    data = response.json()

    assert data["status"] == 500
    assert data["message"] == "Ocorreu um erro interno no servidor."
    assert data["path"] == "/__teste500"
    assert "timestamp" in data