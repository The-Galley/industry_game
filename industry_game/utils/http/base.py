from aiohttp.web import Request


class BaseHttpMixin:
    @property
    def request(self) -> Request:
        raise NotImplementedError
