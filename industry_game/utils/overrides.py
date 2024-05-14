from fastapi.security import APIKeyHeader


class GetSessionFactory:
    pass


class GetGameStorage:
    pass


class GetLobbyStorage:
    pass


class GetUserStorage:
    pass


class GetGameController:
    pass


class GetLoginProvider:
    pass


class MaybeAuth(APIKeyHeader):
    pass


class RequireAuth(APIKeyHeader):
    pass


class RequireAdminAuth(APIKeyHeader):
    pass


class RequirePlayerAuth(APIKeyHeader):
    pass
