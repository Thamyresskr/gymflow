"""
Configuração personalizada do OpenAPI da aplicação GymFlow.
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI):
    """
    Gera um esquema OpenAPI personalizado.
    """

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        summary=app.summary,
        description=app.description,
        routes=app.routes,
    )

    # -------------------------------------------------------------------------
    # Informações da API
    # -------------------------------------------------------------------------

    openapi_schema["info"].update(
        {
            "contact": {
                "name": "Equipe GymFlow",
                "url": "https://github.com/Thamyresskr/gymflow",
                "email": "contato@gymflow.com",
            },
            "license": {
                "name": "MIT",
                "identifier": "MIT",
            },
        }
    )

    # -------------------------------------------------------------------------
    # Servidores
    # -------------------------------------------------------------------------

    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Ambiente de Desenvolvimento",
        }
    ]

    # -------------------------------------------------------------------------
    # Esquema Bearer JWT
    # -------------------------------------------------------------------------

    components = openapi_schema.setdefault("components", {})
    security = components.setdefault("securitySchemes", {})

    security["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": (
            "Informe o token JWT.\n\n"
            "Exemplo:\n"
            "eyJhbGciOiJIUzI1NiIs..."
        ),
    }

    app.openapi_schema = openapi_schema

    return app.openapi_schema