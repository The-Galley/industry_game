from typing import Any, Protocol, TypeVar

from aiohttp.web import HTTPBadRequest, Request
from multidict import MultiMapping
from pydantic import BaseModel, Field, ValidationError

TModel = TypeVar("TModel", bound=BaseModel)


def parse_query_params(model: type[TModel], query: MultiMapping) -> TModel:
    try:
        return model.model_validate(query)
    except ValidationError:
        raise HTTPBadRequest


def parse_json_model(model: type[TModel], data: bytes) -> TModel:
    try:
        return model.model_validate_json(data)
    except ValidationError:
        raise HTTPBadRequest


class PaginationParamsModel(BaseModel):
    page: int = Field(default=1, gt=0)
    page_size: int = Field(default=20, gt=0, le=100)


class AbstractType(Protocol):
    def __init__(self, x: Any) -> None:
        ...


T = TypeVar("T", bound=AbstractType)


def parse_path_param(
    request: Request,
    param_name: str,
    param_type: type[T],
) -> T:
    try:
        return param_type(request.match_info[param_name])
    except ValueError:
        raise HTTPBadRequest
