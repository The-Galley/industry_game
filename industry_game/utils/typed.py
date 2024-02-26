from typing import Any, TypeVar

TObject = TypeVar("TObject", bound=Any)


def not_none(obj: TObject | None) -> TObject:
    if obj is None:
        raise ValueError
    return obj
