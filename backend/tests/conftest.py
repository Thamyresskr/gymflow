"""
Configuração compartilhada para os testes do GymFlow.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.core.dependencies import get_db
from app.main import app

# ============================================================================
# Banco de dados em memória
# ============================================================================

DATABASE_URL = "sqlite://"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# ============================================================================
# Inicialização do banco
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Cria as tabelas antes da execução da suíte.
    """

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


# ============================================================================
# Sessão do banco
# ============================================================================

def override_get_db():
    """
    Dependência utilizada pelos endpoints.
    """

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def db_session():
    """
    Sessão utilizada pelos testes de CRUD e Service.
    """

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# ============================================================================
# Limpeza do banco
# ============================================================================

@pytest.fixture(autouse=True)
def clean_database():
    """
    Limpa todas as tabelas antes de cada teste.
    """

    with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())

    yield


# ============================================================================
# Cliente HTTP
# ============================================================================

@pytest.fixture
def client():
    """
    Cliente HTTP utilizado pelos testes.
    """

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(
        app,
        raise_server_exceptions=False,
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ============================================================================
# Dados padrão
# ============================================================================

@pytest.fixture
def user_data():
    """
    Dados válidos para criação de usuário.
    """

    return {
        "nome": "Aluno Teste",
        "email": "aluno@gymflow.com",
        "senha": "123456",
        "matricula": "20260001",
        "telefone": "11999999999",
    }


@pytest.fixture
def access_token(client, user_data):
    """
    Retorna um token JWT válido.
    """

    client.post(
        "/users/",
        json=user_data,
    )

    response = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["senha"],
        },
    )

    return response.json()["access_token"]


@pytest.fixture
def auth_headers(access_token):
    """
    Cabeçalho Authorization.
    """

    return {
        "Authorization": f"Bearer {access_token}"
    }