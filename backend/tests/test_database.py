from unittest.mock import MagicMock, patch

from app.core.database import get_db


def test_get_db_fecha_sessao():
    fake_db = MagicMock()

    with patch("app.core.database.SessionLocal", return_value=fake_db):
        generator = get_db()

        db = next(generator)

        assert db is fake_db

        try:
            next(generator)
        except StopIteration:
            pass

        fake_db.close.assert_called_once()