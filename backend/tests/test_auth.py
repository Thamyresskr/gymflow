"""
Testes das rotas de autenticação.
"""

from fastapi import status


def criar_usuario(client):
    """
    Cria um usuário para utilização nos testes.
    """

    response = client.post(
        "/users/",
        json={
            "nome": "Administrador",
            "email": "admin@gymflow.com",
            "senha": "123456",
            "matricula": "20260001",
            "telefone": "11999999999",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


def realizar_login(client):
    """
    Realiza login e retorna o token JWT.
    """

    response = client.post(
        "/auth/login",
        data={
            "username": "admin@gymflow.com",
            "password": "123456",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    return response.json()["access_token"]


def test_login_com_sucesso(client):
    """
    Deve autenticar um usuário válido.
    """

    criar_usuario(client)

    response = client.post(
        "/auth/login",
        data={
            "username": "admin@gymflow.com",
            "password": "123456",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 20


def test_login_senha_incorreta(client):
    """
    Não deve autenticar com senha incorreta.
    """

    criar_usuario(client)

    response = client.post(
        "/auth/login",
        data={
            "username": "admin@gymflow.com",
            "password": "senha_errada",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    data = response.json()

    assert data["success"] is False


def test_login_usuario_inexistente(client):
    """
    Não deve autenticar usuário inexistente.
    """

    response = client.post(
        "/auth/login",
        data={
            "username": "naoexiste@gymflow.com",
            "password": "123456",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    data = response.json()

    assert data["success"] is False


def test_acessar_rota_protegida(client):
    """
    Deve acessar uma rota protegida utilizando JWT válido.
    """

    criar_usuario(client)

    token = realizar_login(client)

    response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_token_invalido(client):
    """
    Deve impedir acesso utilizando token inválido.
    """

    response = client.get(
        "/users/",
        headers={
            "Authorization": "Bearer token_invalido",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    data = response.json()

    assert data["success"] is False


def test_sem_token(client):
    """
    Deve impedir acesso sem informar o token.
    """

    response = client.get("/users/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    data = response.json()

    assert data["success"] is False