import discord
from secret import TOKEN
from discord.ext import commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print('   /\\                                                        /\\')
    print('  |  |                                                      |  |')
    print(' /----\\                                                    /----\\')
    print('[______]            Anh sẽ vì em làm thơ tình ái.         [______]')
    print(' |    |         _____                        _____         |    |')
    print(' |[]  |        [     ]                      [     ]        |  []|')
    print(' |    |       [_______][ ][ ][ ][][ ][ ][ ][_______]       |    |')
    print(' |    [ ][ ][ ]|     |  ,----------------,  |     |[ ][ ][ ]    |')
    print(' |             |     |/\'    ____..____    \'\\|     |             |')
    print('  \\  []        |     |    /\'    ||    \'\\    |     |        []  //')
    print('   |      []   |     |   |o     ||     o|   |     |  []       |')
    print('   |           |  _  |   |     _||_     |   |  _  |           |')
    print('   |   []      | (_) |   |    (_||_)    |   | (_) |       []  |')
    print('   |           |     |   |     (||)     |   |     |           |')
    print('   |           |     |   |      ||      |   |     |           |')
    print(' /\'\'           |     |   |o     ||     o|   |     |           \'\'\\')
    print('[_____________[_______]--\'------\'\'------\'--[_______]_____________]')

@client.command()
async def hello(ctx):
    await ctx.send("Hello!")


client.run(TOKEN)

