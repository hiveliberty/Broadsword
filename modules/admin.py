import gc
from memory_profiler import memory_usage
from discord.ext import commands as broadsword
from importlib import reload
from config import config


class Admin:
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.broadsword = bot
        self.server = self.broadsword.get_server(id=config.bot["guild"])

    @broadsword.group(pass_context=True, hidden=False, description='''Группа команд администратора.''')
    async def admin(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.broadsword.say("{0.mention}, invalid git command passed...".format(self.author))

    @admin.command(pass_context=True, name='reload')
    async def _reloadadmin(self, ctx):
        try:
            reload(config)
            self.broadsword.unload_extension(modules.admin)
            self.broadsword.load_extension(modules.admin)
        except Exception as e:
            print(e)
            await self.broadsword.say("Oooops")

    @admin.command(pass_context=True)
    async def test(self, ctx):
        try:
            if config.auth["alertChannel"] is None or config.auth["alertChannel"] == "":
            #if config.auth["alertChannel"] == "":
            #if config.auth["alertChannel"] is None:
                await self.broadsword.send_message(self.server.owner, "Warning! alertChannel is not set!")
        except Exception as e:
            print(e)
            await self.broadsword.say("Oooops")

    @broadsword.group(pass_context=True, hidden=False, description='''Группа команд управления модулями.''')
    async def module(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.broadsword.say("{0.mention}, invalid git command passed...".format(self.author))

    @admin.command(pass_context=True, hidden=False)
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

    @admin.command(pass_context=True, hidden=False)
    async def memory(self, ctx):
        """Memory usage."""
        try:
            self.mem_usage = memory_usage(-1, interval=.2, timeout=1)
            await self.broadsword.say("```Memory usage:\n{}```".format(self.mem_usage))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await self.broadsword.say('```py\n{}\n```'.format(exc))

    @module.command(pass_context=True, hidden=True)
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
            for attr in ('module'):
                self.__dict__.pop(attr,None)

    @module.command(pass_context=True, hidden=True)
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.module = 'modules.' + module
            self.broadsword.unload_extension(self.module)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await self.broadsword.say('```py\n{}\n```'.format(self.module, exc))
        else:
            await self.broadsword.say('\N{OK HAND SIGN}')
            print("Module {} unloaded.".format(module))
        finally:
            for attr in ('module'):
                self.__dict__.pop(attr,None)

    @module.command(pass_context=True, name='reload', hidden=True)
    async def _reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.module = 'modules.' + module
            self.broadsword.unload_extension(self.module)
            self.broadsword.load_extension(self.module)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await self.broadsword.say('```py\n{}\n```'.format(self.module, exc))
        else:
            await self.broadsword.say('\N{OK HAND SIGN}')
            print("Module {} reloaded.".format(module))
        finally:
            for attr in ('module'):
                self.__dict__.pop(attr,None)
            
    @module.command(pass_context=True, name='reloadall', hidden=True)
    async def _reloadall(self, ctx):
        """Reloads all modules."""
        try:
            self.msg = '```Reloaded modules:\n'
            for module, options in config.plugins.items():
                self.broadsword.unload_extension(module)
                if not options.get('enabled', True):
                    continue
                self.broadsword.load_extension(module)
                print("{} reloaded.".format(module))
                self.msg = self.msg + module + '\n'
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            await self.broadsword.say('```py\n{}\n```'.format(module, exc))
        else:
            self.msg = msg + '```'
            await self.broadsword.say("{}".format(self.msg))
        finally:
            for attr in ('module'):
                self.__dict__.pop(attr,None)


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
    broadsword.add_cog(Admin(broadsword))
#    broadsword.add_cog(GCTask(broadsword))
