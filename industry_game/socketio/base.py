from collections.abc import Mapping
from enum import StrEnum
from typing import Any

import socketio
from pydantic import BaseModel, Field

from industry_game.utils.users.storage import PlayerStorage


class SocketioSerializerType(StrEnum):
    DEFAULT = "default"
    MSGPACK = "msgpack"


class DependenciesNamespace(socketio.AsyncNamespace):
    _deps: Mapping[str, Any]

    def __init__(self, deps: Mapping[str, Any], namespace: str | None = None):
        super().__init__(namespace)
        self._deps = deps

    @property
    def sio(self) -> socketio.AsyncServer:
        return self._deps["sio"]

    @property
    def player_storage(self) -> PlayerStorage:
        return self._deps["player_storage"]


class MessageResponse(BaseModel):
    error: bool = False
    error_message: str = ""
    error_body: dict[str, Any] = Field(default_factory=dict)
    body: dict[str, Any] = Field(default_factory=dict)
