from discord.ext import commands

__slots__ = ("Command", "Group", "command", "group")

class Command(commands.Command):
    pass

class Group(commands.Group):
    def command(self, *args, **kwargs):
        return super().command(*args, **kwargs, cls=Command)
    
    def group(self, *args, **kwargs):
        return super().group(*args, **kwargs, cls=self.__class__)

def command(*args, **kwargs):
    return commands.command(*args, **kwargs, cls=Command)

def group(*args, **kwargs):
    return commands.group(*args, **kwargs, cls=Group)
