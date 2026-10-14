
"""
Cria o primeiro usuário ADMIN do GymFlow.

Uso:
    Na pasta backend, execute:
    python create_admin.py

Segurança:
- Não permite criar outro ADMIN se já houver um cadastrado.
- Solicita a senha sem exibi-la no terminal.
- Não armazena senhas em texto puro.
- Reverte a transação em caso de erro.
"""

import re
from getpass import getpass

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

import app.models.checkin  # noqa: F401
import app.models.equipment  # noqa: F401
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import TipoUsuario, User


def email_valido(email: str) -> bool:
    """Valida o formato básico do e-mail."""

    if len(email) > 255:
        return False

    return bool(
        re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email,
        )
    )


def main() -> None:
    """Cria o primeiro administrador, caso ainda não exista."""

    db = SessionLocal()

    try:
        admin = (
            db.query(User)
            .filter(User.tipo == TipoUsuario.ADMIN)
            .first()
        )

        if admin is not None:
            print("Já existe um ADMIN. Nenhuma alteração realizada.")
            return

        nome = input("Nome completo do ADMIN: ").strip()
        email = input("E-mail do ADMIN: ").strip().lower()

        if not nome or len(nome) > 100:
            print("Nome inválido. Informe entre 1 e 100 caracteres.")
            return

        if not email_valido(email):
            print("E-mail inválido.")
            return

        existente = (
            db.query(User)
            .filter(func.lower(User.email) == email)
            .first()
        )

        if existente is not None:
            print("Este e-mail já está cadastrado.")
            return

        senha = getpass("Senha do ADMIN (mínimo 12 caracteres): ")
        confirmacao = getpass("Confirme a senha: ")

        if senha != confirmacao:
            print("As senhas não coincidem.")
            return

        if len(senha) < 12:
            print("A senha precisa ter pelo menos 12 caracteres.")
            return

        if len(senha.encode("utf-8")) > 72:
            print("A senha excede o limite de 72 bytes do bcrypt.")
            return

        novo_admin = User(
            nome=nome,
            email=email,
            senha_hash=hash_password(senha),
            tipo=TipoUsuario.ADMIN,
            ativo=True,
        )

        db.add(novo_admin)
        db.commit()
        db.refresh(novo_admin)

        print("ADMIN criado com sucesso.")
        print(f"ID: {novo_admin.id}")
        print(f"E-mail: {novo_admin.email}")

    except IntegrityError:
        db.rollback()
        print(
            "Conflito de integridade. "
            "Nenhuma alteração pendente foi mantida."
        )

    except SQLAlchemyError:
        db.rollback()
        print(
            "Erro de banco de dados. "
            "A transação foi revertida."
        )

    except Exception:
        db.rollback()
        print(
            "Erro inesperado. "
            "A transação foi revertida; consulte os logs locais."
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()
