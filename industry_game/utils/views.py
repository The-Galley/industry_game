from http import HTTPStatus

from fastapi import Request, Response
from fastapi.templating import Jinja2Templates


class TemplateController:
    def __init__(self, templates: Jinja2Templates) -> None:
        self._templates = templates

    def not_found(self, request: Request, message: str) -> Response:
        return self._templates.TemplateResponse(
            name="./errors/404.html.j2",
            context={
                "message": message,
                "request": request,
            },
            status_code=HTTPStatus.NOT_FOUND,
        )
