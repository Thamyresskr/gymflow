
"""
Testes das rotas de check-ins.
"""

from fastapi import status


def criar_segundo_usuario(client):
    """
    Cria um segundo usuário para testes de autorização.
    """

    response = client.post(
        "/users/",
        json={
            "nome": "Outro Usuário",
            "email": "outro@gymflow.com",
            "senha": "123456",
            "matricula": "20269999",
            "telefone": "11911111111",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    return response


def login_segundo_usuario(client):
    """
    Realiza login do segundo usuário e retorna o header JWT.
    """

    response = client.post(
        "/auth/login",
        data={
            "username": "outro@gymflow.com",
            "password": "123456",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


def test_realizar_checkin(client, auth_headers):
    """Deve realizar um check-in com sucesso."""

    response = client.post(
        "/checkins/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data["id"] > 0
    assert data["checkout_time"] is None


def test_nao_permitir_dois_checkins_abertos(client, auth_headers):
    """Não deve permitir dois check-ins em aberto."""

    client.post(
        "/checkins/",
        headers=auth_headers,
    )

    response = client.post(
        "/checkins/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()

    assert data["status"] == status.HTTP_400_BAD_REQUEST
    assert data["message"] == (
        "O usuário já possui um check-in em aberto."
    )
    assert data["path"] == "/checkins/"
    assert "timestamp" in data


def test_realizar_checkout(client, auth_headers):
    """Deve finalizar o próprio check-in com sucesso."""

    response = client.post(
        "/checkins/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    checkin_id = response.json()["id"]

    response = client.put(
        f"/checkins/{checkin_id}/checkout",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["checkout_time"] is not None


def test_checkout_duplicado(client, auth_headers):
    """Não deve permitir finalizar o mesmo check-in duas vezes."""

    response = client.post(
        "/checkins/",
        headers=auth_headers,
    )

    checkin_id = response.json()["id"]

    response = client.put(
        f"/checkins/{checkin_id}/checkout",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    response = client.put(
        f"/checkins/{checkin_id}/checkout",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()

    assert data["status"] == status.HTTP_400_BAD_REQUEST
    assert data["message"] == (
        "Este check-in já foi finalizado."
    )
    assert data["path"] == f"/checkins/{checkin_id}/checkout"
    assert "timestamp" in data


def test_checkout_inexistente(client, auth_headers):
    """Deve retornar erro para um check-in inexistente."""

    response = client.put(
        "/checkins/9999/checkout",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data["status"] == status.HTTP_404_NOT_FOUND
    assert data["message"] == "Check-in não encontrado."
    assert data["path"] == "/checkins/9999/checkout"
    assert "timestamp" in data


def test_checkout_de_outro_usuario(client, auth_headers):
    """Não deve permitir que um aluno finalize o check-in de outro."""

    response = client.post(
        "/checkins/",
        headers=auth_headers,
    )

    checkin_id = response.json()["id"]

    criar_segundo_usuario(client)
    outro_header = login_segundo_usuario(client)

    response = client.put(
        f"/checkins/{checkin_id}/checkout",
        headers=outro_header,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

    data = response.json()

    assert data["status"] == status.HTTP_403_FORBIDDEN
    assert data["message"] == (
        "Você não possui permissão para finalizar este check-in."
    )
    assert data["path"] == f"/checkins/{checkin_id}/checkout"
    assert "timestamp" in data


def test_listar_checkins_ativos(client, admin_headers, auth_headers):
    """ADMIN deve conseguir listar os check-ins ativos."""

    response_checkin = client.post(
        "/checkins/",
        headers=auth_headers,
    )

    assert response_checkin.status_code == status.HTTP_201_CREATED

    response = client.get(
        "/checkins/ativos",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["checkout_time"] is None


def test_listar_historico(client, admin_headers, auth_headers):
    """ADMIN deve conseguir consultar o histórico completo."""

    response_checkin = client.post(
        "/checkins/",
        headers=auth_headers,
    )

    assert response_checkin.status_code == status.HTTP_201_CREATED

    response = client.get(
        "/checkins/",
        headers=admin_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] > 0


def test_aluno_nao_lista_checkins_ativos(client, auth_headers):
    """ALUNO não deve consultar a lista geral de check-ins ativos."""

    response = client.get(
        "/checkins/ativos",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_aluno_nao_lista_historico_completo(client, auth_headers):
    """ALUNO não deve consultar o histórico completo."""

    response = client.get(
        "/checkins/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_aluno_consulta_proprio_historico(client, auth_headers):
    """ALUNO deve conseguir consultar o próprio histórico."""

    response_checkin = client.post(
        "/checkins/",
        headers=auth_headers,
    )

    assert response_checkin.status_code == status.HTTP_201_CREATED

    response = client.get(
        "/checkins/me",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == response_checkin.json()["id"]
