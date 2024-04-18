import logging

from aiomisc import Service, entrypoint

from industry_game.args import parser
from industry_game.deps import config_deps
from industry_game.services.fastapi_rest import REST

log = logging.getLogger(__name__)


def main() -> None:
    args = parser.parse_args()
    config_deps(args)

    services: list[Service] = [
        REST(
            address=args.api_address,
            port=args.api_port,
            debug=args.debug,
            project_title=args.project_title,
            project_description=args.project_description,
            project_version=args.project_version,
        ),
    ]

    with entrypoint(
        *services,
        log_level=args.log_level,
        log_format=args.log_format,
        pool_size=args.pool_size,
        debug=args.debug,
    ) as loop:
        log.info(
            "REST service started on address %s:%s",
            args.api_address,
            args.api_port,
        )
        loop.run_forever()


if __name__ == "__main__":
    main()
