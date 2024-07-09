from fastapi import APIRouter, Depends, Request, Response
from fastapi.templating import Jinja2Templates

from industry_game.utils.overrides import GetTemplates

router = APIRouter("/")


@router.get("")
async def index_page(
    request: Request,
    templates: Jinja2Templates = Depends(GetTemplates),
) -> Response:
    return templates.TemplateResponse(
        name="./index.html.j2",
        context={
            "request": request,
        },
    )
