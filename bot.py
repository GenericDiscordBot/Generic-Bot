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
import sys
from typing import TYPE_CHECKING

import utils
from utils import Context

if TYPE_CHECKING:
    from utils.types import DiscordPayload

try:
    config_file = sys.argv[1]
except:
    config_file = "./configs/config.toml"

logging.basicConfig(level=logging.INFO)

async def get_prefix(bot: Bot, message: discord.Message):
    if message.guild:
        if not (prefix := await bot.redis.get(str(message.guild.id))):
            async with bot.acquire() as con:
                row = await con.fetchrow("select prefix from guild_configs where guild_id=$1", message.guild.id)
        
            prefix = row["prefix"] if row else bot.config.prefixes.default_prefix
            await bot.redis.set(str(message.guild.id), prefix)
    else:
        prefix = bot.config.prefixes.default_prefix

    return commands.when_mentioned_or(prefix)(bot, message)

class Bot(utils.BotMixin):
    def __init__(self, config: utils.Config, session: aiohttp.ClientSession, redis: aioredis.Redis, pool: asyncpg.Pool):
        super().__init__(command_prefix=get_prefix, **config.bot.args, allowed_mentions=discord.AllowedMentions(**config.bot.allowed_mentions))
        
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

    async def get_context(self, message: discord.Message) -> Context:
        return await super().get_context(message, cls=utils.Context)

    async def on_ready(self):
        self.logger.info(f'Logged on as {self.user} (ID: {self.user.id})')

    async def on_socket_responses(self, msg: DiscordPayload):
        if msg["op"] == 0 and (event := msg["t"]) is not None:
            self.counter[event] += 1

    @commands.command()
    async def ping(self, ctx):
        """ping command"""
        await ctx.send("pong")

    @commands.command()
    async def events(self, ctx):
        events = self.counter.most_common(10)
        events = "\n".join(f"{event}: {amount}" for (event, amount) in events)
        await ctx.send(f"```\n{events}\n```")

    @classmethod
    def run(cls):
        async def runner():
            with open(config_file) as file:
                config = utils.Config(toml.load(file))

            async with aiohttp.ClientSession() as session, aioredis.Redis(**config.redis, decode_responses=True) as redis, asyncpg.create_pool(**config.database) as pool:
                bot = cls(config, session, redis, pool)
                try:
                    await bot.start(config.bot.token)
                finally:
                    await bot.close()
        
        uvloop.install()
        asyncio.run(runner())

    async def get_guild_prefix(self, guild_id: int):
        # in theory this should always exist in the cache if they have a custom prefix as get_prefix loads it into the cache
        return (await self.redis.get(str(guild_id))) or self.config.prefixes.default_prefix
    
    async def set_guild_prefix(self, guild_id: int, prefix: str):
        await self.redis.set(str(guild_id), prefix)
        async with self.acquire() as connection:
            await connection.execute("insert into guild_configs(guild_id, prefix) values ($1, $2) on conflict(guild_id) do update set prefix=$2 where guild_id=$1", guild_id, prefix)

Bot.run()
