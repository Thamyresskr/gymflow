"""
Testes das rotas do Dashboard.
"""

from datetime import UTC, datetime, timedelta

from fastapi import status

from app.models.checkin import Checkin


def test_dashboard_vazio(client, auth_headers):
    """
    Deve retornar indicadores zerados quando não existirem check-ins.
    """

    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    resumo = data["resumo"]

    assert resumo["ocupacao_atual"] == 0
    assert resumo["checkins_hoje"] == 0
    assert resumo["checkouts_hoje"] == 0
    assert resumo["tempo_medio_permanencia"] == 0

    assert data["ultimos_checkins"] == []


def test_dashboard_checkin_ativo(client, auth_headers):
    """
    Deve contabilizar corretamente um check-in ativo.
    """

    response = client.post(
        "/checkins/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    resumo = data["resumo"]

    assert resumo["ocupacao_atual"] == 1
    assert resumo["checkins_hoje"] == 1
    assert resumo["checkouts_hoje"] == 0

    assert len(data["ultimos_checkins"]) == 1

    ultimo = data["ultimos_checkins"][0]

    assert ultimo["usuario"] == "Aluno Teste"
    assert ultimo["saida"] is None


def test_dashboard_checkout(client, auth_headers):
    """
    Deve contabilizar corretamente um checkout realizado.
    """

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

    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    resumo = data["resumo"]

    assert resumo["ocupacao_atual"] == 0
    assert resumo["checkins_hoje"] == 1
    assert resumo["checkouts_hoje"] == 1
    assert resumo["tempo_medio_permanencia"] >= 0


def test_dashboard_tempo_medio(client, auth_headers, db_session):
    """
    Deve calcular corretamente o tempo médio de permanência.
    """

    response = client.post(
        "/checkins/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    checkin_id = response.json()["id"]

    checkin = (
        db_session.query(Checkin)
        .filter(Checkin.id == checkin_id)
        .first()
    )

    assert checkin is not None

    checkin.checkin_time = datetime.now(UTC) - timedelta(minutes=60)
    checkin.checkout_time = datetime.now(UTC)

    db_session.commit()
    db_session.refresh(checkin)

    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["resumo"]["tempo_medio_permanencia"] == 60.0


def test_dashboard_ultimos_checkins(client, auth_headers):
    """
    Deve retornar a lista dos últimos check-ins.
    """

    response = client.post(
        "/checkins/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(
        "/dashboard/",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data["ultimos_checkins"]) == 1

    ultimo = data["ultimos_checkins"][0]

    assert ultimo["usuario"] == "Aluno Teste"
    assert "entrada" in ultimo
    assert "saida" in ultimo