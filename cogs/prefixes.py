
from __future__ import annotations

from discord.ext import commands
import discord
from typing import TYPE_CHECKING

import utils

if TYPE_CHECKING:
    from bot import Bot


class Prefixes(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @utils.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.guild_only()
    async def prefix(self, ctx: utils.Context, new_prefix=None):
        if new_prefix:
            if len(new_prefix) > self.bot.config.prefixes.max_length:
                raise commands.BadArgument("Prefix is too long.")

            await ctx.bot.set_guild_prefix(ctx.guild.id, new_prefix)
            return await ctx.send(f"new prefix set to `{new_prefix}`.")

        prefix = await ctx.bot.get_guild_prefix(ctx.guild.id)
        prefix = prefix or self.bot.config.prefixes.default_prefix

        await ctx.send(f"current prefix is `{prefix}`.")

def setup(bot: Bot):
    bot.add_cog(Prefixes(bot))
