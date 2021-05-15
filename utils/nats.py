import contextlib
from nats.aio.client import Client
import asyncio
from typing import Callable, Any
import json

__slots__ = ("nats_connect", "ClientWrapper")


class ClientWrapper(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._futures: dict[str, list[tuple[Callable, asyncio.Future]]] = {}

    async def wait_for(self, event: str, *, check: Callable, timeout=None) -> Any:
        future = asyncio.Future[Any]()
        futures = self._futures.setdefault(event, [])
        futures.append((check, future))

        async def callback(msg: bytes):
            new_msg = json.loads(msg.decode())
            if await check(new_msg):
                future.set_result(new_msg)
        
        sid = await self.subscribe(event, cb=callback)
        await asyncio.wait_for(future, timeout=timeout)
        await self.unsubscribe(sid)

        return future.result()

    dispatch = Client.publish


@contextlib.asynccontextmanager
async def nats_connect(*args, **kwargs):
    nc = ClientWrapper()
    try:
        await nc.connect(*args, **kwargs)
        yield nc
    finally:
        await nc.close()
