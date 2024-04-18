from fastapi.security import APIKeyHeader


class GetSessionFactory:
    pass


class GetGameStorage:
    pass


class GetUserStorage:
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
