
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
from app.models.user import TipoUsuario, User


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
    """Cria as tabelas antes da execução da suíte."""

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


# ============================================================================
# Sessão do banco
# ============================================================================

def override_get_db():
    """Fornece a sessão de banco de dados aos endpoints de teste."""

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def db_session():
    """Fornece uma sessão para testes de CRUD e serviços."""

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
    """Limpa as tabelas antes de cada teste."""

    with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())

    yield


# ============================================================================
# Cliente HTTP
# ============================================================================

@pytest.fixture
def client():
    """Cria o cliente HTTP de testes."""

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(
            app,
            raise_server_exceptions=False,
        ) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


# ============================================================================
# Dados padrão
# ============================================================================

@pytest.fixture
def user_data():
    """Retorna dados válidos para criação de um ALUNO."""

    return {
        "nome": "Aluno Teste",
        "email": "aluno@gymflow.com",
        "senha": "123456",
        "matricula": "20260001",
        "telefone": "11999999999",
    }


# ============================================================================
# Funções auxiliares de autenticação
# ============================================================================

def criar_usuario_com_perfil(
    client,
    *,
    nome: str,
    email: str,
    senha: str,
    matricula: str,
    telefone: str,
    tipo: TipoUsuario,
):
    """
    Cria um usuário pela API e atribui seu perfil diretamente
    no banco de testes.

    A API pública continua sem permitir que o usuário escolha
    ou eleve o próprio perfil.
    """

    response_cadastro = client.post(
        "/users/",
        json={
            "nome": nome,
            "email": email,
            "senha": senha,
            "matricula": matricula,
            "telefone": telefone,
        },
    )

    assert response_cadastro.status_code == 201, (
        f"Falha ao cadastrar {tipo.value}: "
        f"{response_cadastro.text}"
    )

    db = TestingSessionLocal()

    try:
        usuario = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        assert usuario is not None, (
            f"Usuário de teste não encontrado: {email}"
        )

        usuario.tipo = tipo
        db.commit()
    finally:
        db.close()

    response_login = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": senha,
        },
    )

    assert response_login.status_code == 200, (
        f"Falha no login de {email}: "
        f"{response_login.text}"
    )

    token = response_login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


# ============================================================================
# Autenticação de ALUNO
# ============================================================================

@pytest.fixture
def access_token(client, user_data):
    """Retorna um token JWT válido de ALUNO."""

    response_cadastro = client.post(
        "/users/",
        json=user_data,
    )

    assert response_cadastro.status_code == 201, (
        response_cadastro.text
    )

    response_login = client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["senha"],
        },
    )

    assert response_login.status_code == 200, (
        response_login.text
    )

    return response_login.json()["access_token"]


@pytest.fixture
def auth_headers(access_token):
    """Retorna o cabeçalho de autenticação de ALUNO."""

    return {
        "Authorization": f"Bearer {access_token}",
    }


# ============================================================================
# Autenticação de ADMIN
# ============================================================================

@pytest.fixture
def admin_headers(client):
    """Retorna o cabeçalho de autenticação de ADMIN."""

    return criar_usuario_com_perfil(
        client,
        nome="Administrador de Teste",
        email="admin_teste@gymflow.com",
        senha="123456",
        matricula="ADMTESTE001",
        telefone="11888888888",
        tipo=TipoUsuario.ADMIN,
    )


# ============================================================================
# Autenticação de RECEPCAO
# ============================================================================

@pytest.fixture
def recepcao_headers(client):
    """Retorna o cabeçalho de autenticação de RECEPCAO."""

    return criar_usuario_com_perfil(
        client,
        nome="Recepcionista de Teste",
        email="recepcao_teste@gymflow.com",
        senha="123456",
        matricula="RECTESTE001",
        telefone="11777777777",
        tipo=TipoUsuario.RECEPCAO,
    )


# ============================================================================
# Autenticação de PROFESSOR
# ============================================================================

@pytest.fixture
def professor_headers(client):
    """Retorna o cabeçalho de autenticação de PROFESSOR."""

    return criar_usuario_com_perfil(
        client,
        nome="Professor de Teste",
        email="professor_teste@gymflow.com",
        senha="123456",
        matricula="PROFTESTE001",
        telefone="11666666666",
        tipo=TipoUsuario.PROFESSOR,
    )
