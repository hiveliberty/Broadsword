import gc
import logging
from memory_profiler import memory_usage
from discord.ext import commands as broadsword
from importlib import reload

from config import config

log = logging.getLogger(__name__)

class Admin:
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.broadsword = bot
        self.server = self.broadsword.get_server(id=config.bot["guild"])

    @broadsword.group(pass_context=True, hidden=False, description="Группа команд администратора.")
    async def admin(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.broadsword.say("{0.mention}, invalid command passed...".format(self.author))

    @admin.command(pass_context=True, name='reload')
    async def _reload_a(self, ctx):
        try:
            reload(config)
            self.broadsword.unload_extension(modules.admin)
            self.broadsword.load_extension(modules.admin)
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
            await self.broadsword.say("Oooops! I cann't reload admin module. See logs.")

    @admin.command(pass_context=True, hidden=False)
    async def clearchat(self, ctx):
        """Clear chat."""
        self.mgs = []
        self.number = 100
        try:
            async for x in self.broadsword.logs_from(ctx.message.channel, limit = self.number):
                self.mgs.append(x)
            await self.broadsword.delete_messages(self.mgs)
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
            await self.broadsword.say("Oooops! I cann't clear chat. See logs.")
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

    @broadsword.group(pass_context=True, hidden=False, description='''Группа команд управления модулями.''')
    async def module(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.broadsword.say("{0.mention}, invalid command passed...".format(self.author))

    @module.command(pass_context=True, hidden=True)
    async def load(self, ctx, *, module):
        """Loads a module."""
        self.module = 'modules.' + module
        try:
            self.broadsword.load_extension(self.module)
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
            await self.broadsword.say("Oooops! I cann't load {} module. See logs.".format(module))
        else:
            await self.broadsword.say('\N{OK HAND SIGN}')
            log.info("{} loaded.".format(module))
        finally:
            for attr in ('module'):
                self.__dict__.pop(attr,None)

    @module.command(pass_context=True, hidden=True)
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.module = 'modules.' + module
            self.broadsword.unload_extension(self.module)
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
            await self.broadsword.say("Oooops! I cann't unload {} module. See logs.".format(module))
        else:
            await self.broadsword.say('\N{OK HAND SIGN}')
            log.info("{} unloaded.".format(module))
        finally:
            for attr in ('module'):
                self.__dict__.pop(attr,None)

    @module.command(pass_context=True, name='reload', hidden=True)
    async def _reload_m(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.module = 'modules.' + module
            self.broadsword.unload_extension(self.module)
            self.broadsword.load_extension(self.module)
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
            await self.broadsword.say("Oooops! I cann't reload {} module. See logs.".format(module))
        else:
            await self.broadsword.say('\N{OK HAND SIGN}')
            log.info("{} reloaded.".format(module))
        finally:
            for attr in ('module'):
                self.__dict__.pop(attr,None)
            
    @module.command(pass_context=True, name='reload_all', hidden=True)
    async def _reload_m_all(self, ctx):
        """Reloads all modules."""
        try:
            self.msg = '```Reloaded modules:\n'
            for module, options in config.plugins.items():
                self.broadsword.unload_extension(module)
                if not options.get('enabled', True):
                    continue
                self.broadsword.load_extension(module)
                log.info("{} reloaded.".format(module))
                self.msg = self.msg + module + '\n'
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
            await self.broadsword.say("Oooops! I cann't reload modules. See logs.")
        else:
            self.msg = msg + '```'
            await self.broadsword.say("{}".format(self.msg))
        finally:
            for attr in ('module'):
                self.__dict__.pop(attr,None)


class AdminTask:
    pass


def setup(broadsword):
    broadsword.add_cog(Admin(broadsword))
#    broadsword.add_cog(AdminTask(broadsword))
