
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
    
    @utils.group(aliases=["prefixes", "prefixs"], invoke_without_command=True)
    @commands.guild_only()
    async def prefix(self, ctx: utils.Context):
        """Prefix commands"""
        prefixes = await ctx.bot.get_guild_prefixes(ctx.guild.id)

        string = "\n".join(prefixes)

        await ctx.send(f"Current prefix(s) are:\n{string}")

    @prefix.command()
    async def add(self, ctx: utils.Context, prefix: str):
        """Adds a guild prefix"""
        if len(prefix) > self.bot.config.prefixes.max_length:
            raise commands.BadArgument("Prefix is too long.")

        await ctx.bot.add_guild_prefix(ctx.guild.id, prefix)
        return await ctx.send(f"Added prefix `{prefix}`.")

    @prefix.command()
    async def remove(self, ctx: utils.Context, prefix: str):
        """Removes a guild prefix"""
        status = await self.bot.remove_guild_prefix(ctx.guild.id, prefix)
        if status:
            await ctx.send(f"Removed `{prefix}` from the guilds prefixes.")
        else:
            await ctx.send("That prefix doesnt exist.")

def setup(bot: Bot):
    bot.add_cog(Prefixes(bot))
