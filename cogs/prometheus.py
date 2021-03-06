from __future__ import annotations

import time

import discord
import prometheus_client
import psutil
from aiohttp import web
from discord.ext import commands, tasks

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot import Bot

__slots__ = "setup"

class Prometheus(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

        self.process = psutil.Process()
        self.process.cpu_percent(interval=None)  # to make sure its always filled at the start
        self.ready = False
        self.web = web.Application()
        self.web.router.add_route("GET", "/metrics", self.metrics_handle)
        self.task = self.bot.loop.create_task(web._run_app(self.web, host=bot.config.prometheus.url, port=bot.config.prometheus.port))

        self.guild_stats = prometheus_client.Gauge('counts', documentation='Guild counts', namespace='guild', labelnames=['guild_id', 'count'])

        self.socket_responses = prometheus_client.Counter('socket_responses', documentation='Socket responses', namespace='bot', labelnames=['response'])
        self.socket_events = prometheus_client.Counter('socket_events', documentation='Socket events', namespace='bot', labelnames=['event'])

        self.counters = prometheus_client.Counter('stats', documentation='stats', namespace='bot', labelnames=['stat'])
        self.gauges = prometheus_client.Gauge('counts', documentation='counts', namespace='bot', labelnames=['count'])

        self.op_types = {
            0:  'DISPATCH',
            1:  'HEARTBEAT',
            2:  'IDENTIFY',
            3:  'PRESENCE',
            4:  'VOICE_STATE',
            5:  'VOICE_PING',
            6:  'RESUME',
            7:  'RECONNECT',
            8:  'REQUEST_MEMBERS',
            9:  'INVALIDATE_SESSION',
            10: 'HELLO',
            11: 'HEARTBEAT_ACK',
            12: 'GUILD_SYNC',
        }

        self.stats_thirty_seconds.start()

    def cog_unload(self):
        self.task.cancel()

    async def metrics_handle(self, _):
        data = prometheus_client.generate_latest()
        resp = web.Response(body=data, headers={"Content-type": prometheus_client.CONTENT_TYPE_LATEST})
        return resp

    @commands.Cog.listener()
    async def on_socket_response(self, message: dict) -> None:
        event = message.get('t')
        if event is not None:
            self.socket_events.labels(event=event).inc()

        op_type = self.op_types.get(message.get('op', ''), 'UNKNOWN')

        if op_type == 'HEARTBEAT_ACK':
            self.gauges.labels(count='latency').set(self.bot.latency)

        self.socket_responses.labels(response=op_type).inc()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        if self.ready is True:
            return

        self.ready = True
        self.gauges.labels(count='guilds').set(len(self.bot.guilds))

    @commands.Cog.listener()
    async def on_guild_join(self, _: discord.Guild) -> None:
        self.gauges.labels(count='guilds').inc()

    @commands.Cog.listener()
    async def on_guild_remove(self, _: discord.Guild) -> None:
        self.gauges.labels(count='guilds').dec()

    @commands.Cog.listener()
    async def on_message(self, _: discord.Message) -> None:
        self.counters.labels(stat='messages').inc()

    @commands.Cog.listener()
    async def on_command(self, _: commands.Context) -> None:
        self.counters.labels(stat='commands').inc()

    @commands.Cog.listener()
    async def on_command_completion(self, _: commands.Context) -> None:
        self.counters.labels(stat='commands_completed').inc()

    @commands.Cog.listener()
    async def on_command_error(self, _: commands.Context, error) -> None:

        error = getattr(error, 'original', error)
        if isinstance(error, (commands.CommandNotFound, commands.CommandOnCooldown, commands.MaxConcurrencyReached, commands.CheckFailure)):
            return

        self.counters.labels(stat='commands_errored').inc()

    @tasks.loop(seconds=30)
    async def stats_thirty_seconds(self) -> None:

        await self.bot.wait_until_ready()

        self.gauges.labels(count='uptime').set(round(time.time() - self.bot.start_time))
        self.gauges.labels(count='threads').set(self.process.num_threads())
        self.gauges.labels(count='cpu').set(self.process.cpu_percent(interval=None))

def setup(bot):
    bot.add_cog(Prometheus(bot))
