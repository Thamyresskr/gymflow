"""
Testes das dependências da aplicação.
"""

from app.core.dependencies import get_db


def test_get_db():
    """
    Deve criar e fechar uma sessão do banco de dados.
    """

    generator = get_db()

    db = next(generator)

    assert db is not None

    # Força a execução do bloco finally
    generator.close()