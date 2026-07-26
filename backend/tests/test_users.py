"""
Testes das rotas de gerenciamento de usuários.
"""

from uuid import uuid4

from fastapi import status


def criar_usuario(client):
    """
    Cria um usuário de teste.
    """

    identificador = uuid4().hex[:8]

    response = client.post(
        "/users/",
        json={
            "nome": f"Usuário Teste {identificador}",
            "email": f"usuario_{identificador}@gymflow.com",
            "senha": "123456",
            "matricula": f"M{identificador}",
            "telefone": "11999999999",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    return response.json()


def test_listar_usuarios(
    client,
    auth_headers,
):
    """
    Deve listar usuários autenticados.
    """

    response = client.get(
        "/users/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_buscar_usuario_por_id(
    client,
    auth_headers,
):
    """
    Deve buscar usuário pelo ID.
    """

    usuario = criar_usuario(client)

    response = client.get(
        f"/users/{usuario['id']}",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == usuario["id"]
    assert data["email"] == usuario["email"]


def test_buscar_usuario_inexistente(
    client,
    auth_headers,
):
    """
    Deve retornar erro ao buscar usuário inexistente.
    """

    response = client.get(
        "/users/99999",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data["message"] == "Usuário não encontrado."


def test_atualizar_usuario(
    client,
    auth_headers,
):
    """
    Deve atualizar dados de usuário.
    """

    usuario = criar_usuario(client)

    response = client.put(
        f"/users/{usuario['id']}",
        headers=auth_headers,
        json={
            "nome": "Usuário Atualizado",
            "telefone": "11888888888",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["nome"] == "Usuário Atualizado"
    assert data["telefone"] == "11888888888"


def test_atualizar_usuario_email_existente(
    client,
    auth_headers,
):
    """
    Não permite atualizar usuário usando e-mail já existente.
    """

    usuario1 = criar_usuario(client)
    usuario2 = criar_usuario(client)

    response = client.put(
        f"/users/{usuario2['id']}",
        headers=auth_headers,
        json={
            "email": usuario1["email"],
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data["message"] == "E-mail já cadastrado."


def test_excluir_usuario(
    client,
    auth_headers,
):
    """
    Deve excluir usuário existente.
    """

    usuario = criar_usuario(client)

    response = client.delete(
        f"/users/{usuario['id']}",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_excluir_usuario_inexistente(
    client,
    auth_headers,
):
    """
    Deve retornar erro ao excluir usuário inexistente.
    """

    response = client.delete(
        "/users/99999",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data["message"] == "Usuário não encontrado."