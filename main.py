import discord
from secret import TOKEN, CHANNEL_NAME
from discord.ext import commands
import asyncio
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def create_or_get_channel(guild, channel_name):
    existing_channel = discord.utils.get(guild.voice_channels, name=channel_name)
    
    if existing_channel:
        return existing_channel

    new_channel = await guild.create_voice_channel(name=channel_name)
    return new_channel

@client.event
async def on_ready():
    global GUILD
    global GUILD_ID
    global GUILD_NAME
    GUILD = client.guilds[0]
    GUILD_ID = GUILD.id
    GUILD_NAME = GUILD.name
    channel = await create_or_get_channel(GUILD, CHANNEL_NAME)
    print(f"Channel '{channel.name}' with ID '{channel.id}' created/obtained.")
    print(f"Bot is ready. Logged in as {client.user}.")

async def disconnect_if_empty(voice_channel):
    await asyncio.sleep(15)  # Wait for 15 seconds
    if len(voice_channel.members) == 1:  # Only the bot is present in the channel
        await voice_channel.guild.voice_client.disconnect()
        print(f'Disconnected from voice channel: {voice_channel.name}')

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:  # User joined a voice channel
        if after.channel.name == CHANNEL_NAME:
            voice_channel = after.channel
            await join_voice_channel(voice_channel)
            await disconnect_if_empty(voice_channel)

async def join_voice_channel(voice_channel):
    if voice_channel.guild.voice_client is None:
        await voice_channel.connect()
        print(f'Joined voice channel: {voice_channel.name}')

client.run(TOKEN)

