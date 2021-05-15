
from __future__ import annotations

from discord.ext import commands
import discord
from typing import TYPE_CHECKING

import utils

if TYPE_CHECKING:
    from bot import Bot

__slots__ = "setup"

class Prefixes(commands.Cog):
    __slots__ = "bot"

    def __init__(self, bot: Bot):
        self.bot = bot
    
    @utils.group(invoke_without_command=True)
    @commands.guild_only()
    async def prefix(self, ctx: utils.Context, new_prefix: str = None):
        """Prefix commands"""

        if new_prefix:
            if len(new_prefix) > self.bot.config.prefixes.max_length:
                raise commands.BadArgument("Prefix is too long.")

            await ctx.bot.set_guild_prefix(ctx.guild.id, new_prefix)
            return await ctx.send(f"Set prefix to `{new_prefix}`.")
            
        prefix = await ctx.bot.get_guild_prefix(ctx.guild.id)

        await ctx.send(f"Current prefix is: {prefix}")


def setup(bot: Bot):
    bot.add_cog(Prefixes(bot))
