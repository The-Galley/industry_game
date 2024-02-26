from typing import Any

import msgspec


class CustomStruct(msgspec.Struct, frozen=True):
    def to_dict(self) -> dict[str, Any]:
        return {f: getattr(self, f) for f in self.__struct_fields__}
