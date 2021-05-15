from discord.ext import menus
import discord

from typing import Callable, Iterable, Tuple, Generic, TypeVar

__slots__ = "CallbackPaginator"

_T = TypeVar("_T")

class CallbackPaginator(menus.ListPageSource, Generic[_T]):
    """A paginator that generates infomation via callbacks

    Parameters
    -----------
    data: Iterable[Any]
        The data to be passed to the callback
    callback: Callable[[Any], Tuple[str, str]]
    """
    __slots__ = ("name", "value", "attrs")
    def __init__(self, data: Iterable[_T], callback: Callable[[_T], Tuple[str, str]], **attrs):
        super().__init__(data, per_page=5)
        self.callback = callback
        self.attrs = attrs

    async def format_page(self, menu: menus.MenuPages, entries):
        embed = discord.Embed(**self.attrs)
        for entry in entries:
            name, value = self.callback(entry)
            embed.add_field(name=name, value=value, inline=False)
            embed.set_footer(icon_url=str(menu.ctx.bot.user.avatar.replace(format="png")), text=f"page {menu.current_page+1}/{self.get_max_pages()}")

        return embed
