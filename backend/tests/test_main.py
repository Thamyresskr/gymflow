from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app, listar_rotas

client = TestClient(app)


def test_home():
    """
    Deve retornar a mensagem de status da API.
    """
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": f"{settings.APP_NAME} funcionando!"
    }


def test_listar_rotas(capsys):
    """
    Deve listar todas as rotas registradas na aplicação.
    """
    listar_rotas()

    captured = capsys.readouterr()

    assert "Rotas registradas" in captured.out

    # Garante que algumas rotas da aplicação foram listadas.
    assert "/" in captured.out
    assert "/auth/login" in captured.out
    assert "/users" in captured.out