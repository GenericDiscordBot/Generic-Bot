from __future__ import annotations

from discord.ext import tasks, commands
import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple, Any
    from .bot import BotMixin

__slots__ = "Reminder"

class Reminder(commands.Cog):
    def __init__(self, bot: BotMixin):
        self.bot = bot
        self.name = self.__class__.__name__.lower()
        self.loop.start()
    
    def get_query(self) -> str:
        """Should delete and get all rows where the reminder is finished"""
        return f"delete from {self.name} where end_time <= now() returning *"

    def insert_query(self, end_time: datetime.datetime, *data) -> Tuple[str, Tuple[Any, ...]]:
        values = [f'${i}' for i in range(1, len(data) + 2)]
        return f"insert into {self.name} values ({','.join(values)})", (*data, end_time)

    async def add_reminder(self, end_time, *data):
        query, args = self.insert_query(end_time, *data)
        async with self.bot.acquire() as connection:
            return await connection.execute(query, *args)

    @tasks.loop(minutes=1)
    async def loop(self):
        async with self.bot.acquire() as connection:
            rows = await connection.fetch(self.get_query())
            for row in rows:
                self.bot.dispatch(f"on_{self.name}", row)

    @loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()
