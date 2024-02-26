from collections.abc import Mapping
from functools import partial
from http import HTTPStatus

import msgspec
from aiohttp.web_response import Response, json_response

from industry_game.utils.json import dumps

JSON_CONTENT_TYPE = "application/json"
ENCODING = "utf-8"

_encoder = msgspec.json.Encoder()


def msgspec_json_response(
    obj: msgspec.Struct,
    status: int = HTTPStatus.OK,
    headers: Mapping[str, str] | None = None,
) -> Response:
    return Response(
        body=_encoder.encode(obj),
        content_type=JSON_CONTENT_TYPE,
        charset=ENCODING,
        headers=headers,
        status=status,
    )


fast_json_response = partial(json_response, dumps=dumps)
