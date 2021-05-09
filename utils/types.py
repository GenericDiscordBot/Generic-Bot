from typing import TypedDict, Optional

__slots__ = "DiscordPayload"

class DiscordPayload(TypedDict):
    op: int
    d: dict
    s: Optional[int]
    t: Optional[str]

