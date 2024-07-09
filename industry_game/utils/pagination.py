from pydantic import BaseModel


class MetaPagination(BaseModel):
    total: int
