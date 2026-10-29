
"""
Testes das rotas de gerenciamento de equipamentos do GymFlow.
"""

from uuid import uuid4

from fastapi import status


def dados_equipamento():
    """Gera dados válidos e únicos para um equipamento."""
    identificador = uuid4().hex[:8]

    return {
        "nome": f"Esteira Teste {identificador}",
        "categoria": "cardio",
        "fabricante": "Movement",
        "modelo": "RT250",
        "patrimonio": f"EQ-{identificador}",
        "numero_serie": f"SN-{identificador}",
        "observacao": "Equipamento criado em teste automatizado.",
    }


def criar_equipamento(client, admin_headers):
    """Cria um equipamento usando o perfil ADMIN."""
    response = client.post(
        "/equipments/",
        headers=admin_headers,
        json=dados_equipamento(),
    )

    assert response.status_code == status.HTTP_201_CREATED, response.text
    return response.json()


# ============================================================================
# Cadastro de equipamentos
# ============================================================================

def test_admin_pode_cadastrar_equipamento(client, admin_headers):
    """ADMIN pode cadastrar equipamentos."""
    response = client.post(
        "/equipments/",
        headers=admin_headers,
        json=dados_equipamento(),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["categoria"] == "cardio"
    assert response.json()["status"] == "ativo"


def test_recepcao_nao_pode_cadastrar_equipamento(
    client,
    recepcao_headers,
):
    """RECEPCAO não pode cadastrar equipamentos."""
    response = client.post(
        "/equipments/",
        headers=recepcao_headers,
        json=dados_equipamento(),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_aluno_nao_pode_cadastrar_equipamento(client, auth_headers):
    """ALUNO não pode cadastrar equipamentos."""
    response = client.post(
        "/equipments/",
        headers=auth_headers,
        json=dados_equipamento(),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_anonimo_nao_pode_cadastrar_equipamento(client):
    """Cadastro de equipamento exige autenticação."""
    response = client.post(
        "/equipments/",
        json=dados_equipamento(),
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ============================================================================
# Listagem de equipamentos
# ============================================================================

def test_admin_pode_listar_equipamentos(client, admin_headers):
    """ADMIN pode listar equipamentos."""
    criar_equipamento(client, admin_headers)

    response = client.get(
        "/equipments/",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_recepcao_pode_listar_equipamentos(
    client,
    admin_headers,
    recepcao_headers,
):
    """RECEPCAO pode listar equipamentos."""
    criar_equipamento(client, admin_headers)

    response = client.get(
        "/equipments/",
        headers=recepcao_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_aluno_nao_pode_listar_equipamentos(client, auth_headers):
    """ALUNO não pode listar equipamentos."""
    response = client.get(
        "/equipments/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_anonimo_nao_pode_listar_equipamentos(client):
    """Listagem de equipamentos exige autenticação."""
    response = client.get("/equipments/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ============================================================================
# Consulta de equipamento por ID
# ============================================================================

def test_admin_pode_consultar_equipamento(
    client,
    admin_headers,
):
    """ADMIN pode consultar um equipamento pelo ID."""
    equipamento = criar_equipamento(client, admin_headers)

    response = client.get(
        f"/equipments/{equipamento['id']}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == equipamento["id"]


def test_recepcao_pode_consultar_equipamento(
    client,
    admin_headers,
    recepcao_headers,
):
    """RECEPCAO pode consultar um equipamento pelo ID."""
    equipamento = criar_equipamento(client, admin_headers)

    response = client.get(
        f"/equipments/{equipamento['id']}",
        headers=recepcao_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == equipamento["id"]


def test_aluno_nao_pode_consultar_equipamento(
    client,
    auth_headers,
):
    """ALUNO não pode consultar equipamentos por ID."""
    response = client.get(
        "/equipments/1",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_anonimo_nao_pode_consultar_equipamento(client):
    """Consulta de equipamento exige autenticação."""
    response = client.get("/equipments/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ============================================================================
# Atualização de equipamentos
# ============================================================================

def test_admin_pode_atualizar_equipamento(client, admin_headers):
    """ADMIN pode atualizar equipamentos."""
    equipamento = criar_equipamento(client, admin_headers)

    response = client.put(
        f"/equipments/{equipamento['id']}",
        headers=admin_headers,
        json={"observacao": "Atualizado pelo teste."},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["observacao"] == "Atualizado pelo teste."


def test_recepcao_nao_pode_atualizar_equipamento(
    client,
    admin_headers,
    recepcao_headers,
):
    """RECEPCAO não pode atualizar equipamentos."""
    equipamento = criar_equipamento(client, admin_headers)

    response = client.put(
        f"/equipments/{equipamento['id']}",
        headers=recepcao_headers,
        json={"observacao": "Tentativa não autorizada."},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_aluno_nao_pode_atualizar_equipamento(
    client,
    admin_headers,
    auth_headers,
):
    """ALUNO não pode atualizar equipamentos."""
    equipamento = criar_equipamento(client, admin_headers)

    response = client.put(
        f"/equipments/{equipamento['id']}",
        headers=auth_headers,
        json={"observacao": "Tentativa não autorizada."},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_anonimo_nao_pode_atualizar_equipamento(
    client,
    admin_headers,
):
    """Atualização de equipamento exige autenticação."""
    equipamento = criar_equipamento(client, admin_headers)

    response = client.put(
        f"/equipments/{equipamento['id']}",
        json={"observacao": "Tentativa não autorizada."},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ============================================================================
# Exclusão de equipamentos
# ============================================================================

def test_admin_pode_excluir_equipamento(client, admin_headers):
    """ADMIN pode excluir equipamentos."""
    equipamento = criar_equipamento(client, admin_headers)

    response = client.delete(
        f"/equipments/{equipamento['id']}",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_recepcao_nao_pode_excluir_equipamento(
    client,
    admin_headers,
    recepcao_headers,
):
    """RECEPCAO não pode excluir equipamentos."""
    equipamento = criar_equipamento(client, admin_headers)

    response = client.delete(
        f"/equipments/{equipamento['id']}",
        headers=recepcao_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_aluno_nao_pode_excluir_equipamento(
    client,
    admin_headers,
    auth_headers,
):
    """ALUNO não pode excluir equipamentos."""
    equipamento = criar_equipamento(client, admin_headers)

    response = client.delete(
        f"/equipments/{equipamento['id']}",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_anonimo_nao_pode_excluir_equipamento(
    client,
    admin_headers,
):
    """Exclusão de equipamento exige autenticação."""
    equipamento = criar_equipamento(client, admin_headers)

    response = client.delete(
        f"/equipments/{equipamento['id']}",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
