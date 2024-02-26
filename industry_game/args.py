import argparse

import configargparse
from aiomisc.log import LogFormat, LogLevel
from yarl import URL

parser = configargparse.ArgumentParser(
    allow_abbrev=False,
    auto_env_var_prefix="APP_",
    description="Server Industry",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument("-D", "--debug", action="store_true", default=True)
parser.add_argument(
    "-s",
    "--pool-size",
    type=int,
    default=8,
    help="Thread pool size",
)

group = parser.add_argument_group("Logging options")
group.add_argument(
    "--log-level",
    default=LogLevel.debug,
    choices=LogLevel.choices(),
)
group.add_argument(
    "--log-format",
    default=LogFormat.color,
    choices=LogFormat.choices(),
)

group = parser.add_argument_group("API options")
group.add_argument("--api-address", default="127.0.0.1")
group.add_argument("--api-port", type=int, default=8000)

group = parser.add_argument_group("PostgreSQL options")
group.add_argument("--pg-dsn", required=True, type=URL)

group = parser.add_argument_group("Security")
group.add_argument("--secret", type=str, default="secret")
