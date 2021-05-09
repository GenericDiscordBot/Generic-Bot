#!/usr/bin/env python3.9

from __future__ import annotations

from discord.ext import commands
import aiohttp
import discord
import asyncio
import collections
import asyncpg
import toml
import os
import logging
import aioredis
import uvloop
from typing import TYPE_CHECKING

import utils

if TYPE_CHECKING:
    from utils.types import DiscordPayload

__slots__ = "Bot"

logging.basicConfig(level=logging.INFO)

async def get_prefix(bot: Bot, message: discord.Message):
    prefixes: list[str]

    if message.guild:
        if (prefixes := await bot.redis.lrange(str(message.guild.id), 0, -1)) is None:
            async with bot.acquire() as con:
                rows = await con.fetch("select prefix from prefixes where guild_id=$1", message.guild.id)

            if rows:
                prefixes = [row["prefix"] for row in rows]
            else:
                prefixes = bot.config.prefixes.default_prefixes

            await bot.redis.rpush(str(message.guild.id), *prefixes)
    else:
        prefixes = bot.config.prefixes.default_prefix

    return commands.when_mentioned_or(*prefixes)(bot, message)

class Bot(utils.BotMixin):
    def __init__(self, config: utils.Config, session: aiohttp.ClientSession, redis: aioredis.Redis, pool: asyncpg.Pool, **kwargs):
        super().__init__(command_prefix=get_prefix, **config.bot.args | kwargs, allowed_mentions=discord.AllowedMentions(**config.bot.allowed_mentions))
        
        self.config = config
        
        self.webhook = discord.Webhook.from_url(self.config.logging.webhook_url, session=session)
        handler = utils.WebhookHandler(self.webhook, self.config.logging.levels)
        logging.getLogger("discord").addHandler(handler)
        self.logger = logging.getLogger("generic_bot")
        self.logger.addHandler(handler)

        self.redis = redis
        self.session = session
        self.pool = pool
        self.counter = collections.Counter[str]()
        
        for key, value in self.config.environment.items():
            os.environ[key] = value

        for extension in self.config.bot.extensions:
            self.load_extension(extension)

        self.all_commands["eval"] = self.get_command("jsk py")
        self.get_command("eval").hidden = True  # type: ignore

    async def get_context(self, message: discord.Message) -> utils.Context:
        return await super().get_context(message, cls=utils.Context)

    async def on_ready(self):
        self.logger.info(f'Logged on as {self.user} (ID: {self.user.id})')

    async def on_socket_responses(self, msg: DiscordPayload):
        if msg["op"] == 0 and (event := msg["t"]) is not None:
            self.counter[event] += 1

    @commands.command()
    async def ping(self, ctx):
        """ping command"""
        await ctx.send("Pong")

    @commands.command()
    async def events(self, ctx):
        """Shows all events the bot has received"""
        events = self.counter.most_common(10)
        events = "\n".join(f"{event}: {amount}" for (event, amount) in events)
        await ctx.send(f"```\n{events}\n```")

    @classmethod
    def run(cls, config_file: str, **kwargs):
        async def runner():
            with open(config_file) as file:
                config = utils.Config(toml.load(file))

            async with aiohttp.ClientSession() as session, aioredis.Redis(**config.redis, decode_responses=True) as redis, asyncpg.create_pool(**config.database) as pool:
                bot = cls(config, session, redis, pool, **kwargs)
                try:
                    await bot.start(config.bot.token)
                finally:
                    await bot.close()
        
        uvloop.install()
        asyncio.run(runner())

    async def get_guild_prefixes(self, guild_id: int) -> list[str]:
        # in theory this should always exist in the cache if they have a custom prefix as get_prefix loads it into the cache
        return await self.redis.lrange(str(guild_id), 0, -1)
    
    async def add_guild_prefix(self, guild_id: int, prefix: str):
        await self.redis.lpush(str(guild_id), prefix)
        async with self.acquire() as connection:
            await connection.execute("insert into prefixes(guild_id, prefix) values ($1, $2)", guild_id, prefix)

    async def remove_guild_prefix(self, guild_id: int, prefix: str) -> bool:
        status = await self.redis.lrem(str(guild_id), 0, prefix)
        if status:
            async with self.acquire() as connection:
                await connection.execute("delete from prefixes where guild_id=$1 and prefix=$2", guild_id, prefix)
        
        return bool(status)

    async def on_guild_join(self, guild: discord.Guild):
        await self.redis.lpush(str(guild.id), *self.config.prefixes.default_prefixes)
        async with self.acquire() as connection:
            await connection.execute("insert into guild_configs(guild_id) values($1)", guild.id)

            default_prefixes = self.config.prefixes.default_prefixes

            prefixes = iter(default_prefixes)
            values = [(guild.id, next(prefixes)) for _ in range(len(default_prefixes))]

            await connection.executemany("insert into prefixes(guild_id, prefix) values($1, $2)", values)
