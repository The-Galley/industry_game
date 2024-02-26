import pytest
import socketio


@pytest.fixture
def sio() -> socketio.AsyncServer:
    return socketio.AsyncServer(async_mode="aiohttp")
