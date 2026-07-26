"""
Testes do arquivo principal da aplicação.
"""

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app

client = TestClient(app)


def test_home():
    """
    Deve retornar informações da API.
    """

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == settings.APP_NAME
    assert data["version"] == settings.VERSION
    assert data["status"] == "online"
    assert data["docs"] == "/docs"
    assert data["redoc"] == "/redoc"


def test_documentacao():
    """
    Deve disponibilizar a documentação Swagger.
    """

    response = client.get("/docs")

    assert response.status_code == 200