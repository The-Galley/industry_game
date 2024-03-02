from http import HTTPStatus

from aiohttp.test_utils import TestClient
from aiomisc_pytest import TCPProxy

API_URL = "/api/v1/ping/"


async def test_ping_db_ok_status(api_client: TestClient) -> None:
    response = await api_client.get(API_URL)
    assert response.status == 200


async def test_ping_db_ok_data(api_client: TestClient) -> None:
    response = await api_client.get(API_URL)
    result = await response.json()
    assert result == {"db": True}


async def test_ping_db_disconnect_error_status(
    api_client: TestClient, pg_proxy: TCPProxy
) -> None:
    with pg_proxy.slowdown(2, 2):
        response = await api_client.get(API_URL)
        assert response.status == HTTPStatus.INTERNAL_SERVER_ERROR


async def test_ping_db_disconnect_error_format(
    api_client: TestClient, pg_proxy: TCPProxy
) -> None:
    with pg_proxy.slowdown(2, 2):
        response = await api_client.get(API_URL)
        result = await response.json()
        assert result == {"db": False}
