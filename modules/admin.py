from memory_profiler import memory_usage
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
        self.module = 'modules.' + module
        try:
            self.broadsword.load_extension(self.module)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await self.broadsword.say('```py\n{}\n```'.format(self.module, exc))
        else:
            await self.broadsword.say('\N{OK HAND SIGN}')
            print("Module {} loaded.".format(module))
        finally:
            del self.module

    @broadsword.command(pass_context=True, hidden=True)
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        self.module = 'modules.' + module
        try:
            self.broadsword.unload_extension(self.module)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await self.broadsword.say('```py\n{}\n```'.format(self.module, exc))
        else:
            await self.broadsword.say('\N{OK HAND SIGN}')
            print("Module {} unloaded.".format(module))
        finally:
            del self.module

    @broadsword.command(pass_context=True, name='reload', hidden=True)
    async def _reload(self, ctx, *, module):
        """Reloads a module."""
        self.module = 'modules.' + module
        try:
            self.broadsword.unload_extension(self.module)
            self.broadsword.load_extension(self.module)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await self.broadsword.say('```py\n{}\n```'.format(self.module, exc))
        else:
            await self.broadsword.say('\N{OK HAND SIGN}')
            print("Module {} reloaded.".format(module))
        finally:
            del self.module
            
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
        del self.mgs
        
    @broadsword.command(pass_context=True, hidden=False)
    async def clearchat(self, ctx):
        """Clear chat."""
        self.mgs = []
        self.number = 100
        try:
            async for x in self.broadsword.logs_from(ctx.message.channel, limit = self.number):
                self.mgs.append(x)
            await self.broadsword.delete_messages(self.mgs)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await self.broadsword.say('```py\n{}\n```'.format(exc))
        finally:
            del self.mgs

    @broadsword.command(pass_context=True, hidden=False)
    async def memory(self, ctx):
        """Memory usage."""
        try:
            self.mem_usage = memory_usage(-1, interval=.2, timeout=1)
            await self.broadsword.say("```Memory usage:\n{}```".format(self.mem_usage))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await self.broadsword.say('```py\n{}\n```'.format(exc))
            
def setup(broadsword):
    broadsword.add_cog(Admin(broadsword, plugins))
