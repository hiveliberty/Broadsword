from discord.ext import commands as broadsword
from config.config import plugins as plugins
#import asyncio
#import traceback
#import discord
#import inspect
#import textwrap
#from contextlib import redirect_stdout
#import io

# to expose to the eval command
#import datetime
#from collections import Counter

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
        for module, options in self.plugins.items():
            if not options.get('enabled', True):
                continue
            try:
                self.broadsword.unload_extension(module)
                self.broadsword.load_extension(module)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                await self.broadsword.say('```py\n{}\n```'.format(module, exc))
            else:
                print("{} reloaded.".format(module))
        await self.broadsword.say("All modules reloaded.")

def setup(broadsword):
    broadsword.add_cog(Admin(broadsword, plugins))
