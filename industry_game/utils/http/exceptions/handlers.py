from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from industry_game.utils.http.models import StatusResponse


async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    return exception_json_response(
        status_code=exc.status_code, message=exc.detail
    )


def exception_json_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=StatusResponse(message=message).model_dump(),
    )
