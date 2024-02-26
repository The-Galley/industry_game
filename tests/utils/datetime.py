from datetime import datetime


def format_tz(dt: datetime | None) -> str | None:
    if dt is not None:
        return dt.isoformat().replace("+00:00", "Z")
    return None
