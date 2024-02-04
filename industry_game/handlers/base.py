from aiohttp.web import Request

from industry_game.storages.ping import PingStorage


class BaseHttpMixin:
    @property
    def request(self) -> Request:
        raise NotImplementedError


class DependenciesMixin(BaseHttpMixin):
    @property
    def ping_storage(self) -> PingStorage:
        return self.request.app["ping_storage"]
