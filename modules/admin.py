from discord.ext import commands as broadsword
from config.config import plugins as plugins

class Admin:
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot, plugins):
        self.broadsword = bot
        self.plugins = plugins

    @broadsword.command(pass_context=True, hidden=True)
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.broadsword.load_extension(module)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await self.broadsword.say('```py\n{}\n```'.format(module, exc))
        else:
            await self.broadsword.say('\N{OK HAND SIGN}')
            print("{} loaded.".format(module))

    @broadsword.command(pass_context=True, hidden=True)
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.broadsword.unload_extension(module)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await self.broadsword.say('```py\n{}\n```'.format(module, exc))
        else:
            await self.broadsword.say('\N{OK HAND SIGN}')
            print("{} unloaded.".format(module))

    @broadsword.command(pass_context=True, name='reload', hidden=True)
    async def _reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.broadsword.unload_extension(module)
            self.broadsword.load_extension(module)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await self.broadsword.say('```py\n{}\n```'.format(module, exc))
        else:
            await self.broadsword.say('\N{OK HAND SIGN}')
            print("{} reloaded.".format(module))
            
    @broadsword.command(pass_context=True, name='reloadall', hidden=True)
    async def _reloadall(self, ctx):
        """Reloads all modules."""
        msg = '```Reloaded modules:\n'
        for module, options in self.plugins.items():
            try:
                self.broadsword.unload_extension(module)
                if not options.get('enabled', True):
                    continue
                self.broadsword.load_extension(module)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                await self.broadsword.say('```py\n{}\n```'.format(module, exc))
            else:
                print("{} reloaded.".format(module))
                msg = msg + module + '\n'
        msg = msg + '```'
        await self.broadsword.say("{}".format(msg))

def setup(broadsword):
    broadsword.add_cog(Admin(broadsword, plugins))
