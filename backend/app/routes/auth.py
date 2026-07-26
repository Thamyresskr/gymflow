"""
Rotas relacionadas à autenticação.

Responsabilidades:
- Receber as requisições de autenticação dos usuários.
- Validar os dados de entrada.
- Delegar as regras de autenticação para a camada de serviços.
- Retornar o token JWT quando a autenticação for realizada com sucesso.
"""

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.auth import Token
from app.schemas.error import ErrorResponse
from app.services.auth_service import login_user

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"],
)


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Autenticar usuário",
    description="""
Realiza a autenticação de um usuário utilizando e-mail e senha.

Após a autenticação bem-sucedida, a API retorna um token JWT.
Esse token deve ser enviado no cabeçalho HTTP **Authorization**
no seguinte formato:

Bearer <token>

O token será utilizado para acessar todos os endpoints protegidos
da aplicação.
""",
    responses={
        status.HTTP_200_OK: {
            "description": "Autenticação realizada com sucesso.",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Credenciais inválidas.",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "model": ErrorResponse,
            "description": "Erro de validação dos dados enviados.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponse,
            "description": "Erro interno do servidor.",
        },
    },
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """
    Autentica um usuário utilizando suas credenciais.

    Recebe as credenciais enviadas pelo formulário OAuth2,
    encaminha a autenticação para a camada de serviços e
    retorna um token JWT quando o login é realizado com sucesso.

    Args:
        form_data: Credenciais informadas pelo usuário.
        db: Sessão ativa do banco de dados.

    Returns:
        Token: Token JWT utilizado para autenticação nas
        demais requisições da API.
    """

    return login_user(
        db=db,
        email=form_data.username,
        senha=form_data.password,
    )