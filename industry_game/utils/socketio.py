import logging
from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import BaseModel

Model = TypeVar("Model", bound=BaseModel)

log = logging.getLogger(__name__)


def validate_data(model_type: type[Model], data: Mapping[str, Any]) -> Model:
    return model_type.model_validate(data)
