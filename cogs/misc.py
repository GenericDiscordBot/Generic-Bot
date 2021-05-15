
from __future__ import annotations

from discord.ext import commands
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

__slots__ = "setup"

class Misc(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        """ping command"""
        await ctx.send("Pong")

    @commands.command()
    async def events(self, ctx):
        """Shows all events the bot has received"""
        events = ctx.bot.counter.most_common(10)
        events = "\n".join(f"{event}: {amount}" for (event, amount) in events)
        await ctx.send(f"```\n{events}\n```")


def setup(bot: Bot):
    bot.add_cog(Misc(bot))
