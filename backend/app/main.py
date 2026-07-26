"""
Arquivo principal da aplicação GymFlow.

Responsabilidades:
- Inicializar a API
- Registrar as rotas
- Criar as tabelas do banco de dados
- Registrar os handlers globais de exceções
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.core.exception_handlers import register_exception_handlers
from app.core.logger import logger
from app.core.middleware import LoggingMiddleware

# ============================================================================
# Modelos
# ============================================================================

import app.models.checkin  # noqa: F401
import app.models.user  # noqa: F401

# ============================================================================
# Rotas
# ============================================================================

from app.routes.auth import router as auth_router
from app.routes.checkins import router as checkin_router
from app.routes.dashboard import router as dashboard_router
from app.routes.health import router as health_router
from app.routes.users import router as user_router

# ============================================================================
# Banco de Dados
# ============================================================================

Base.metadata.create_all(bind=engine)

logger.info("Banco de dados inicializado.")

# ============================================================================
# OpenAPI / Swagger
# ============================================================================

tags_metadata = [
    {
        "name": "Sistema",
        "description": "Endpoints responsáveis pelo monitoramento e status da API.",
    },
    {
        "name": "Health",
        "description": "Monitoramento da saúde da aplicação.",
    },
    {
        "name": "Autenticação",
        "description": "Autenticação de usuários e geração de tokens JWT.",
    },
    {
        "name": "Usuários",
        "description": "Cadastro e gerenciamento de usuários.",
    },
    {
        "name": "Check-ins",
        "description": "Controle de entrada e saída dos usuários.",
    },
    {
        "name": "Dashboard",
        "description": "Indicadores e estatísticas de ocupação da academia.",
    },
]

# ============================================================================
# Aplicação
# ============================================================================

app = FastAPI(
    title=settings.APP_NAME,
    summary="API REST para gerenciamento de academias.",
    description="""
# 🏋️ GymFlow API

Sistema desenvolvido em **FastAPI** para gerenciamento de academias.

## Funcionalidades

- 👤 Cadastro de usuários
- 🔐 Autenticação JWT
- ✅ Check-in
- 🚪 Check-out
- 📊 Dashboard
- ❤️ Health Check
- 📚 Documentação automática via OpenAPI

## Tecnologias

- FastAPI
- SQLAlchemy
- SQLite
- JWT
- OAuth2
- Pytest

## Objetivo

Disponibilizar uma API segura, documentada e preparada para integração com aplicações Web e Mobile.
""",
    version=settings.VERSION,
    contact={
        "name": "Equipe GymFlow",
        "email": "contato@gymflow.com",
    },
    license_info={
        "name": "MIT License",
    },
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

logger.info("%s iniciada com sucesso.", settings.APP_NAME)

# ============================================================================
# CORS
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS registrado.")

# ============================================================================
# Middleware
# ============================================================================

app.add_middleware(LoggingMiddleware)

logger.info("Middleware de logging registrado.")

# ============================================================================
# Tratamento Global de Exceções
# ============================================================================

register_exception_handlers(app)

logger.info("Handlers globais de exceções registrados.")

# ============================================================================
# Registro das Rotas
# ============================================================================

routers = (
    health_router,
    auth_router,
    user_router,
    checkin_router,
    dashboard_router,
)

for router in routers:
    app.include_router(router)

logger.info("%d grupos de rotas registrados.", len(routers))

# ============================================================================
# Sistema
# ============================================================================


@app.get(
    "/",
    tags=["Sistema"],
    summary="Status da API",
    description="""
Verifica se a API está em execução.

Este endpoint pode ser utilizado para testes rápidos
e monitoramento da aplicação.
""",
    response_description="Mensagem de status da API.",
)
async def home():
    """
    Endpoint utilizado para verificar se a API está online.
    """

    logger.info("Endpoint '/' acessado.")

    return {
        "message": f"{settings.APP_NAME} funcionando!"
    }


# ============================================================================
# Desenvolvimento
# ============================================================================


def listar_rotas():
    """
    Exibe todas as rotas registradas na aplicação.
    """

    logger.info("Listando rotas registradas.")

    print("\nRotas registradas:\n")

    for route in sorted(app.routes, key=lambda r: r.path):
        methods = ",".join(sorted(route.methods))
        print(f"{route.path:35} {methods}")


if __name__ == "__main__":  # pragma: no cover
    listar_rotas()