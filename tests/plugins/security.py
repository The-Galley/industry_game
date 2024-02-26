import pytest

from industry_game.utils.security import Passgen


@pytest.fixture
def passgen(secret: str) -> Passgen:
    return Passgen(secret=secret)
