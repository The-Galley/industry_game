import msgspec


class StatusResponse(msgspec.Struct):
    message: str
