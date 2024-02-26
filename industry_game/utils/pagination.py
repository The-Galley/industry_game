import math

from industry_game.utils.msgspec import CustomStruct


class MetaPagination(CustomStruct, frozen=True):
    page: int
    pages: int
    total: int
    page_size: int

    @classmethod
    def create(cls, page: int, page_size: int, total: int) -> "MetaPagination":
        return MetaPagination(
            page=page,
            page_size=page_size,
            total=total,
            pages=int(math.ceil(total / page_size)) or 1,
        )
