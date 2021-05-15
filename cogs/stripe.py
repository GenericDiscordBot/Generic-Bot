
from __future__ import annotations

from discord.ext import commands
import discord
from typing import TYPE_CHECKING

import utils

if TYPE_CHECKING:
    from bot import Bot

__slots__ = "setup"

class Stripe(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def __ainit__(self):
        await self.bot.nats.subscribe("stripe", cb=self.stripe_callback)

    async def stripe_callback(self, msg):
        print(msg)

def setup(bot: Bot):
    bot.add_cog(Stripe(bot))
