
"""
Configuração personalizada do OpenAPI da aplicação GymFlow.
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI):
    """
    Gera um esquema OpenAPI personalizado para a aplicação GymFlow.
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

    # Informações da API
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

    # Servidor de desenvolvimento
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Ambiente de Desenvolvimento",
        }
    ]

    # Esquema de autenticação Bearer JWT
    openapi_schema.setdefault("components", {})
    openapi_schema["components"].setdefault(
        "securitySchemes", {}
    )

    openapi_schema["components"]["securitySchemes"][
        "BearerAuth"
    ] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    app.openapi_schema = openapi_schema

    return app.openapi_schema
