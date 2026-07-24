from passlib.context import CryptContext

# Configuração do algoritmo de criptografia
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Gera o hash de uma senha.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verifica se a senha informada corresponde ao hash armazenado.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )