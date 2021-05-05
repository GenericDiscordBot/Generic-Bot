from discord.ext import commands


class Command(commands.Command):
    pass

class Group(commands.Group):
    pass

def command(*args, **kwargs):
    return commands.command(*args, **kwargs, cls=Command)

def group(*args, **kwargs):
    return commands.group(*args, **kwargs, cls=Group)
