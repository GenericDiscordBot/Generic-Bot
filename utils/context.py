from __future__ import annotations

from discord.ext import commands
import discord
from typing import TYPE_CHECKING

from .bot import BotMixin

if TYPE_CHECKING:
    from asyncpg import Pool
    from bot import Bot
    from typing import Optional

__slots__ = "Context"

class Context(commands.Context):
    bot: Bot

    @property
    def pool(self) -> Pool:
        pool = self.bot.pool
        assert pool

        return pool

    acquire = BotMixin.acquire

    async def send(self, content_or_embed: Optional[str | discord.Embed] = None, **kwargs):
        if isinstance(content_or_embed, discord.Embed):
            kwargs["embed"] = content_or_embed
            content_or_embed = None
        
        return await super().send(content_or_embed, **kwargs)
