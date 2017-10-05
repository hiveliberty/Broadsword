VERSION = "0.3.1.b00002"

import discord
import asyncio
#import pman
client = discord.Client()

#Инклуды======================================================================
from config import config
from lib import eve_utils
from lib import utils






#=============================================================================
#Евенты дискорда==============================================================
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Version v.' + VERSION)
    print('------')
    #SETTING GAME
    await client.change_presence(game=discord.Game(name='EVE Online'))
@client.event
async def on_socket_raw_receive(msg):
    tick()
    #print('rawr')
@client.event
async def on_socket_raw_send(msg):
    tick()
    #print('raws')
@client.event
async def on_message(message): #TODO - обработчик комманд
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!tq'):
        status = await eve_utils.getTQOnline()
        stmp = "%s **TQ Status:**  %d players online. **Version:** %s" % (message.author.mention, status['userCount'], status['serverVersion'])
        await client.send_message(message.channel, stmp)
    elif message.content.startswith('!info'):
        stmp = "%s I am %s with firmware version v%s" % (message.author.mention,client.user.name, VERSION)
        await client.send_message(message.channel, stmp)
    elif message.content.startswith('!charinfo'):
        param = await utils.cmdGetParams(message.content)
        info = await eve_utils.getCharInfo(param)
        await client.send_message(message.channel, "%s %s" % (message.author.mention, info ))
    elif message.content.startswith('!not'):
        stmp = await eve_utils.getNotifications()
        await client.send_message(message.channel,"response is: %s" % stmp)
#==============================================================================
#Таймер - т.к. исполнение клиента дискорда это уже отдельный цикл, у меня пока не хватает скилла прикрутить точный таймер
#так, чтобы не нарушить работу бота, поэтому используем способ без циклов и таймеров от старины Y_Less :)
#==============================================================================
def tick():
    #if minsPassed(30) ==true:
        pass
        
client.run(config.Bot_Token)



