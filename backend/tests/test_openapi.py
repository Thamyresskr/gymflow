"""
Testes da configuração personalizada do OpenAPI.
"""

from fastapi import FastAPI

from app.core.openapi import custom_openapi


def test_custom_openapi_gera_schema():
    """
    Deve gerar um schema OpenAPI personalizado.
    """

    app = FastAPI(
        title="GymFlow Test",
        version="1.0.0",
        summary="Teste",
        description="API de teste",
    )

    schema = custom_openapi(app)

    assert schema is not None

    assert schema["info"]["title"] == "GymFlow Test"
    assert schema["info"]["version"] == "1.0.0"

    assert "contact" in schema["info"]

    assert schema["info"]["contact"]["name"] == (
        "Equipe GymFlow"
    )

    assert schema["info"]["license"]["name"] == "MIT"


def test_custom_openapi_configura_servidor():
    """
    Deve configurar o servidor padrão da API.
    """

    app = FastAPI()

    schema = custom_openapi(app)

    assert "servers" in schema

    assert schema["servers"][0]["url"] == (
        "http://localhost:8000"
    )

    assert schema["servers"][0]["description"] == (
        "Ambiente de Desenvolvimento"
    )


def test_custom_openapi_configura_jwt():
    """
    Deve registrar autenticação Bearer JWT.
    """

    app = FastAPI()

    schema = custom_openapi(app)

    security = (
        schema["components"]
        ["securitySchemes"]
        ["BearerAuth"]
    )

    assert security["type"] == "http"
    assert security["scheme"] == "bearer"
    assert security["bearerFormat"] == "JWT"


def test_custom_openapi_retorna_schema_existente():
    """
    Deve retornar o schema já criado sem gerar novamente.
    """

    app = FastAPI()

    schema_original = {
        "teste": True
    }

    app.openapi_schema = schema_original

    schema = custom_openapi(app)

    assert schema == schema_original