from __future__ import annotations

import discord
from discord.ext import commands, menus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from utils import Context

__slots__ = ("setup", "teardown")

class BotHelpCommand(menus.ListPageSource):
    __slots__ = ("name", "value", "attrs")
    def __init__(self, data, name, value, **attrs):
        super().__init__(data, per_page=5)
        self.name = name
        self.value = value
        self.attrs = attrs

    async def format_page(self, menu: menus.MenuPages, entries):
        embed = discord.Embed(**self.attrs)
        for entry in entries:
            embed.add_field(name=self.name(entry), value=self.value(entry), inline=False)
            embed.set_footer(icon_url=str(menu.ctx.bot.user.avatar.replace(format="png")), text=f"page {menu.current_page+1}/{self.get_max_pages()}")

        return embed

class HelpCommand(commands.HelpCommand):
    context: Optional[Context]

    async def send_bot_help(self, mapping):
        coms = [command for commands in mapping.values() for command in commands]

        coms = await self.filter_commands(coms, sort=True)

        pages = menus.MenuPages(BotHelpCommand(coms,
            lambda command: f"{command.name} {command.signature}",
            lambda command: command.help.split("\n")[0], title="Commands"),
            clear_reactions_after=True, timeout=120, delete_message_after=True)

        await pages.start(self.context)
    
    async def send_group_help(self, group: commands.Group):
        coms = await self.filter_commands(group.commands, sort=True)

        pages = menus.MenuPages(BotHelpCommand(coms,
            lambda command: f"{command.name} {command.signature}",
            lambda command: command.help.split("\n")[0], description=group.help+"\n\n", title=group.name),
            clear_reactions_after=True, timeout=120, delete_message_after=True)

        await pages.start(self.context)

    async def send_command_help(self, command):
        embed = discord.Embed(description=command.help, title=f"{command.name} {command.signature}")
        embed.set_footer(icon_url=str(self.context.bot.user.avatar.replace(format="png")))
        await self.context.send(embed)


def setup(bot):
    bot.help_command = HelpCommand(command_attrs={"hidden": True})

def teardown(bot):
    bot.help_command = commands.DefaultHelpCommand()
