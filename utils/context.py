from __future__ import annotations

from discord.ext import commands
from typing import TYPE_CHECKING
from .bot import Bot as BotBase

if TYPE_CHECKING:
    from asyncpg import Pool
    from bot import Bot

__slots__ = "Context"

class Context(commands.Context):
    bot: Bot

    @property
    def pool(self) -> Pool:
        pool = self.bot.pool
        assert pool

        return pool

    acquire = BotBase.acquire
