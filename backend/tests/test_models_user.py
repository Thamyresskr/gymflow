from app.models.user import TipoUsuario, User


def test_user_repr():
    user = User(
        id=1,
        nome="João Silva",
        email="joao@email.com",
        senha_hash="hash123",
        tipo=TipoUsuario.ADMIN,
        ativo=True,
    )

    resultado = repr(user)

    assert "User(" in resultado
    assert "id=1" in resultado
    assert "nome='João Silva'" in resultado
    assert "email='joao@email.com'" in resultado
    assert "tipo='admin'" in resultado
    assert "ativo=True" in resultado