import math
from typing import Self

from pydantic import BaseModel


class MetaPagination(BaseModel):
    page: int
    pages: int
    total: int
    page_size: int

    @classmethod
    def create(cls, page: int, page_size: int, total: int) -> Self:
        return cls(
            page=page,
            page_size=page_size,
            total=total,
            pages=int(math.ceil(total / page_size)) or 1,
        )
