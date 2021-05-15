from __future__ import annotations

from discord.ext import commands
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncpg import Pool, Connection

__slots__ = "Bot"
class Bot(commands.Bot):
    pool: Pool

    @asynccontextmanager
    async def acquire(self):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                connection: Connection
                yield connection
