from argparse import Namespace

import pytest

from industry_game.args import parser


@pytest.fixture
def secret() -> str:
    return "secret"


@pytest.fixture
def args() -> Namespace:
    return parser.parse_args([])
