"""
Arquivo principal da aplicação GymFlow.

Responsabilidades:
- Inicializar a API
- Registrar as rotas
- Criar as tabelas do banco de dados
- Registrar os handlers globais de exceções
"""

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.core.exception_handlers import register_exception_handlers
from app.core.logger import logger

# ============================================================================
# Modelos
# ============================================================================

import app.models.checkin
import app.models.user

# ============================================================================
# Rotas
# ============================================================================

from app.routes.auth import router as auth_router
from app.routes.checkins import router as checkin_router
from app.routes.dashboard import router as dashboard_router
from app.routes.users import router as user_router

# ============================================================================
# Banco de Dados
# ============================================================================

Base.metadata.create_all(bind=engine)

logger.info("Banco de dados inicializado.")

# ============================================================================
# Aplicação
# ============================================================================

app = FastAPI(
    title=settings.APP_NAME,
    description="""
API para gerenciamento de academias.

## Funcionalidades

- 👤 Cadastro de usuários
- 🔐 Autenticação JWT
- ✅ Check-in
- 🚪 Checkout
- 📊 Dashboard gerencial

## Tecnologias

- FastAPI
- SQLAlchemy
- SQLite
- JWT
- OAuth2
""",
    version=settings.VERSION,
)

logger.info("%s iniciada com sucesso.", settings.APP_NAME)

# ============================================================================
# Tratamento Global de Exceções
# ============================================================================

register_exception_handlers(app)

logger.info("Handlers globais de exceções registrados.")

# ============================================================================
# Registro das Rotas
# ============================================================================

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(checkin_router)
app.include_router(dashboard_router)

logger.info("Rotas registradas com sucesso.")

# ============================================================================
# Sistema
# ============================================================================


@app.get(
    "/",
    tags=["Sistema"],
    summary="Status da API",
    description="Verifica se a API está em execução.",
)
def home():
    """
    Endpoint utilizado para verificar se a API está online.
    """
    logger.info("Endpoint '/' acessado.")
    return {"message": f"{settings.APP_NAME} funcionando!"}


# ============================================================================
# Desenvolvimento
# ============================================================================


def listar_rotas():
    """
    Exibe todas as rotas registradas na aplicação.
    """
    logger.info("Listando rotas registradas.")

    print("\nRotas registradas:\n")

    for route in app.routes:
        print(route.path)


if __name__ == "__main__":  # pragma: no cover
    listar_rotas()