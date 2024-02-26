import hashlib
import logging

log = logging.getLogger(__name__)


class Passgen:
    _secret: str
    _max_length: int

    def __init__(self, secret: str, max_length: int = 256) -> None:
        self._secret = secret
        self._max_length = max_length

    def hashpw(self, password: str) -> str:
        hashable_str = (password + self._secret).encode()
        return hashlib.sha256(hashable_str).hexdigest()[: self._max_length]
