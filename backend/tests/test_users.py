
"""
Testes das rotas de gerenciamento de usuários.
"""

from uuid import uuid4

from fastapi import status


def criar_usuario(client):
    """
    Cria um usuário de teste pelo cadastro público.
    O perfil inicial deve ser ALUNO.
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

    usuario = response.json()
    assert usuario["tipo"] == "aluno"

    return usuario


# ============================================================================
# Listagem de usuários
# ============================================================================

def test_listar_usuarios(
    client,
    admin_headers,
):
    """
    ADMIN deve conseguir listar usuários.
    """

    criar_usuario(client)

    response = client.get(
        "/users/",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 2


def test_aluno_nao_pode_listar_usuarios(
    client,
    auth_headers,
):
    """
    ALUNO não pode listar todos os usuários.
    """

    response = client.get(
        "/users/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# ============================================================================
# Consulta por identificador
# ============================================================================

def test_buscar_usuario_por_id(
    client,
    admin_headers,
):
    """
    ADMIN deve conseguir buscar um usuário pelo ID.
    """

    usuario = criar_usuario(client)

    response = client.get(
        f"/users/{usuario['id']}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == usuario["id"]
    assert data["email"] == usuario["email"]


def test_buscar_usuario_inexistente(
    client,
    admin_headers,
):
    """
    ADMIN deve receber 404 ao buscar um usuário inexistente.
    """

    response = client.get(
        "/users/99999",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data["message"] == "Usuário não encontrado."


def test_aluno_nao_pode_buscar_usuario_por_id(
    client,
    auth_headers,
):
    """
    ALUNO não pode consultar usuários pela rota administrativa.
    """

    response = client.get(
        "/users/99999",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# ============================================================================
# Atualização de usuários
# ============================================================================

def test_atualizar_usuario(
    client,
    admin_headers,
):
    """
    ADMIN deve conseguir atualizar dados de um usuário.
    """

    usuario = criar_usuario(client)

    response = client.put(
        f"/users/{usuario['id']}",
        headers=admin_headers,
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
    admin_headers,
):
    """
    Não permite atualizar um usuário com e-mail já cadastrado.
    """

    usuario1 = criar_usuario(client)
    usuario2 = criar_usuario(client)

    response = client.put(
        f"/users/{usuario2['id']}",
        headers=admin_headers,
        json={
            "email": usuario1["email"],
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data["message"] == "E-mail já cadastrado."


def test_aluno_nao_pode_atualizar_usuario(
    client,
    auth_headers,
):
    """
    ALUNO não pode atualizar usuários pela rota administrativa.
    """

    usuario = criar_usuario(client)

    response = client.put(
        f"/users/{usuario['id']}",
        headers=auth_headers,
        json={
            "nome": "Tentativa de alteração",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# ============================================================================
# Exclusão de usuários
# ============================================================================

def test_excluir_usuario(
    client,
    admin_headers,
):
    """
    ADMIN deve conseguir excluir um usuário de teste.
    """

    usuario = criar_usuario(client)

    response = client.delete(
        f"/users/{usuario['id']}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_excluir_usuario_inexistente(
    client,
    admin_headers,
):
    """
    ADMIN deve receber 404 ao excluir um usuário inexistente.
    """

    response = client.delete(
        "/users/99999",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data["message"] == "Usuário não encontrado."


def test_aluno_nao_pode_excluir_usuario(
    client,
    auth_headers,
):
    """
    ALUNO não pode excluir usuários.
    """

    usuario = criar_usuario(client)

    response = client.delete(
        f"/users/{usuario['id']}",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


# ============================================================================
# Dados do próprio usuário
# ============================================================================

def test_aluno_pode_consultar_proprios_dados(
    client,
    auth_headers,
):
    """
    ALUNO autenticado pode consultar os próprios dados.
    """

    response = client.get(
        "/users/me",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["tipo"] == "aluno"
