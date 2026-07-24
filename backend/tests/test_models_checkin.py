from datetime import UTC, datetime

from app.models.checkin import Checkin


def test_checkin_repr():
    entrada = datetime(2026, 1, 1, 10, 0, tzinfo=UTC)
    saida = datetime(2026, 1, 1, 11, 0, tzinfo=UTC)

    checkin = Checkin(
        id=1,
        user_id=10,
        checkin_time=entrada,
        checkout_time=saida,
    )

    assert repr(checkin) == (
        f"Checkin(id=1, "
        f"user_id=10, "
        f"checkin={entrada}, "
        f"checkout={saida})"
    )