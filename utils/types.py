from typing import TypedDict, Optional

class DiscordPayload(TypedDict):
    op: int
    d: dict
    s: Optional[int]
    t: Optional[str]

