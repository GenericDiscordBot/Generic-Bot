from __future__ import annotations

from discord.ext import commands
from functools import wraps
import copy
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncpg import Pool, Connection

__slots__ = ("BotMeta", "BotMixin")

class BotMeta(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        bot = super().__new__(cls, name, bases, attrs)
        bot.__inline_commands__ = []  # type: ignore

        for name in dir(bot):
            value = getattr(bot, name)

            if isinstance(value, commands.Command):
                value.callback = cls.wrapper(bot, value)
                value.params = dict(list(value.params.items())[1:])  # .popitem(last=False)

                setattr(bot, name, value)
                bot.__inline_commands__.append(value)  # type: ignore

        bot.__inline_kwargs__ = kwargs  # type: ignore
        return bot

    @staticmethod
    def wrapper(bot, value):
        callback = copy.copy(value.callback)
        @wraps(value.callback)
        def custom_callback(*args, **kwargs):
            return callback(bot, *args, **kwargs)
        
        return custom_callback

class BotMixin(commands.Bot, metaclass=BotMeta):
    pool: Pool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **self.__inline_kwargs__ | kwargs)  # type: ignore
        self._inject()

    def _inject(self):
        for command in self.__inline_commands__:  # type: ignore
            self.add_command(command)

    @asynccontextmanager
    async def acquire(self):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                connection: Connection
                yield connection
