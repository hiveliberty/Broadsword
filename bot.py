VERSION = "0.3.1.b05"

import discord
from discord.ext import commands

from lib.evelib import EVE_Basic
#from lib import utils

from config import config

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Version v.' + VERSION)
    print('------')

@bot.command(pass_context=True)
async def evestatus(ctx):
    try:
        author = ctx.message.author
        status = await EVE_Basic.getTQOnline()
        stmp = '{0.mention} **TQ Status:**  {1} players online. **Version:** {2}'.format(author, status['userCount'], status['serverVersion'])
        await bot.say(stmp)
    except:
        print('Error with obtain eve status')
        
@bot.command(pass_context=True)
async def charinfo(ctx, char):
#    try:
        author = ctx.message.author
        info = await EVE_Basic.getCharInfo(char)
        stmp = '{0.mention} \n {1}'.format(author, info)
        await bot.say(stmp)
#    except:
#        print('Error with obtain eve status')

bot.run(config.token)
bot.close()