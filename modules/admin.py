import gc
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

class GCTask:
    def __init__(self, bot):
        self.broadsword = bot
        self._task = self.broadsword.loop.create_task(self.taskGC())
        print('QueueMessages.taskGC should have been run..')
        
    def __unload(self):
        self._task.cancel()
        print('QueueMessages.taskGC should have been unloaded..')

    async def taskGC(self):
        try:
            while not self.broadsword.is_closed:
                gc.collect()
                self.gc_stat = gc.get_stats()
                print("GC stat: {}".format(self.gc_stat))
                del self.mem_usage
                await asyncio.sleep(60)
        except asyncio.CancelledError as e:
            print(e)
        except (OSError, discord.ConnectionClosed):
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.taskGC())
            
def setup(broadsword):
    broadsword.add_cog(Admin(broadsword, plugins))
#    broadsword.add_cog(GCTask(broadsword))