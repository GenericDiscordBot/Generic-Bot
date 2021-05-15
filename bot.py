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
import time
from typing import TYPE_CHECKING

import utils

if TYPE_CHECKING:
    from utils.types import DiscordPayload

__slots__ = "Bot"

logging.basicConfig(level=logging.INFO)

async def get_prefix(bot: Bot, message: discord.Message):
    if message.guild:
        if (prefix := await bot.redis.get(str(message.guild.id))) is None:
            async with bot.acquire() as con:
                prefix = await con.fetchval("select prefix from prefixes where guild_id=$1", message.guild.id)

                if not prefix:
                    prefix = bot.config.prefixes.default_prefix

                await bot.redis.set(str(message.guild.id), prefix)
    else:
        prefix = bot.config.prefixes.default_prefix

    return commands.when_mentioned_or(prefix)(bot, message)

class Bot(utils.Bot):
    def __init__(self, config: utils.Config, session: aiohttp.ClientSession, redis: aioredis.Redis, pool: asyncpg.Pool, nats: utils.ClientWrapper, **kwargs):
        super().__init__(command_prefix=get_prefix, **config.bot.args, **kwargs, allowed_mentions=discord.AllowedMentions(**config.bot.allowed_mentions))
        
        self.config = config
        
        self.webhook = discord.Webhook.from_url(self.config.logging.webhook_url, session=session)
        handler = utils.WebhookHandler(self.webhook, self.config.logging.levels)
        logging.getLogger("discord").addHandler(handler)
        self.logger = logging.getLogger("generic_bot")
        self.logger.addHandler(handler)

        self.nats = nats
        self.redis = redis
        self.session = session
        self.pool = pool
        self.counter = collections.Counter[str]()
        self.start_time = time.time()

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

    async def on_socket_response(self, msg: DiscordPayload):
        if msg["op"] == 0 and (event := msg["t"]) is not None:
            self.counter[event] += 1

    @classmethod
    def run(cls, config_file: str, **kwargs):
        async def runner():
            with open(config_file) as file:
                config = utils.Config(toml.load(file))

            async with aiohttp.ClientSession() as session, aioredis.Redis(**config.redis, decode_responses=True) as redis, asyncpg.create_pool(**config.database) as pool, utils.nats_connect(config.nats.url) as nats:
                bot = cls(config, session, redis, pool, nats, **kwargs)

                for cog in bot.cogs.values():
                    if func := getattr(cog, "__ainit__", None):
                        await func()

                try:
                    await bot.start(config.bot.token)
                finally:
                    await bot.close()

        uvloop.install()
        asyncio.run(runner())

    async def get_guild_prefix(self, guild_id: int) -> list[str]:
        # in theory this should always exist in the cache if they have a custom prefix as get_prefix loads it into the cache
        return await self.redis.get(str(guild_id))
    
    async def set_guild_prefix(self, guild_id: int, prefix: str):
        await self.redis.set(str(guild_id), prefix)
        async with self.acquire() as connection:
            await connection.execute("insert into prefixes(guild_id, prefix) values ($1, $2) on conflict (guild_id) do update set prefix=$2 where prefixes.guild_id=$1", guild_id, prefix)

    async def remove_guild_prefix(self, guild_id: int, prefix: str) -> bool:
        # see get_guild_prefix on why i can pin this on redis
        status = await self.redis.delete(str(guild_id))
        if status:
            async with self.acquire() as connection:
                await connection.execute("delete from prefixes where guild_id=$1 and prefix=$2", guild_id, prefix)
        
        return bool(status)
