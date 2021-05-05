from __future__ import annotations

import discord
from discord.ext import commands, menus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from utils import Context

class BotHelpCommand(menus.ListPageSource):
    def __init__(self, data, ctx, name, value, **attrs):
        super().__init__(data, per_page=5)
        self.ctx = ctx
        self.name = name
        self.value = value
        self.attrs = attrs

    async def format_page(self, menu, entries):
        embed = discord.Embed(**self.attrs)
        for entry in entries:
            embed.add_field(name=self.name(entry), value=self.value(entry), inline=False)
            embed.set_footer(icon_url=str(self.ctx.bot.user.avatar_url_as(format="png")), text=f"page {menu.current_page+1}/{self.get_max_pages()}")

        return embed

class HelpCommand(commands.HelpCommand):
    command_attrs = {"hidden": True}
    context: Optional[Context]

    async def send_bot_help(self, mapping):
        coms = [command for commands in mapping.values() for command in commands]

        pages = menus.MenuPages(BotHelpCommand(coms, self.context,
            lambda command: f"{command.name} {command.signature}",
            lambda command: command.help.split("\n")[0], title="Commands"),
            clear_reactions_after=True, timeout=120)

        await pages.start(self.context)
    
    async def send_group_help(self, group: commands.Group):
        pages = menus.MenuPages(BotHelpCommand(list(group.commands), self.context,
            lambda command: f"{command.name} {command.signature}",
            lambda command: command.help.split("\n")[0], description=group.help+"\n\n", title=group.name),
            clear_reactions_after=True, timeout=120)

        await pages.start(self.context)

    async def send_command_help(self, command):
        embed = discord.Embed(description=command.help, title=f"{command.name} {command.signature}")
        embed.set_footer(icon_url=str(self.context.bot.user.avatar.replace(format="png")))
        await self.context.send(embed)


def setup(bot):
    bot.help_command = HelpCommand()

def teardown(bot):
    bot.help_command = commands.DefaultHelpCommand()
