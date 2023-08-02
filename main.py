import discord
from secret import TOKEN
from discord.ext import commands
import asyncio
from discord import FFmpegPCMAudio
#TOKEN = os.environ['TOKEN']
CHANNEL_NAME = '⭐｜Vào để xây lâu đài tình ái'

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
CONNECT = False

async def create_or_get_channel(guild, channel_name):
    existing_channel = discord.utils.get(guild.voice_channels, name=channel_name)
    
    if existing_channel:
        return existing_channel

    new_channel = await guild.create_voice_channel(name=channel_name)
    return new_channel

@client.event
async def on_ready():
    global GUILD_INFO
    global AUDIO_SOURCE
    global CONNECT
    CONNECT = False
    GUILD_INFO = {}

    for guild in client.guilds:
        GUILD_INFO[guild.id] = {
            'guild': guild,
            'channel': await create_or_get_channel(guild, CHANNEL_NAME)
        }
        print(f"Channel '{GUILD_INFO[guild.id]['channel'].name}' with ID '{GUILD_INFO[guild.id]['channel'].id}' created/obtained for Guild '{guild.name}' with ID '{guild.id}'.")
    audio_file = "LauDaiTinhAi.opus"
    print(f"Bot is ready. Logged in as {client.user}.")

async def disconnect_if_empty(voice_channel):
    global CONNECT
    await asyncio.sleep(15)  # Wait for 15 seconds
    if len(voice_channel.members) == 1:  # Only the bot is present in the channel
        voice_client = voice_channel.guild.voice_client

        if voice_client.is_playing():
            voice_client.stop()
        CONNECT = False
        await voice_client.disconnect()
        print(f'Disconnected from voice channel: {voice_channel.name}')

async def play_audio(voice_channel, audio_file):
    voice_client = voice_channel.guild.voice_client

    while True:
        if not voice_client or not voice_client.is_connected():
            return

        audio_source = discord.FFmpegPCMAudio(audio_file)
        voice_client.play(audio_source)

        while voice_client.is_playing():
            await asyncio.sleep(1)

        # Add a 3-second delay before playing the audio again
        await asyncio.sleep(3)

@client.event
async def on_voice_state_update(member, before, after):
    global CONNECT
    print(CONNECT)
    if before.channel is not None and after.channel is None:  # User left a voice channel
        if CONNECT:
            await disconnect_if_empty(before.channel)
    elif before.channel is None and after.channel is not None:  # User joined a voice channel
        if after.channel.name == CHANNEL_NAME:
            voice_channel = after.channel
            if not CONNECT:
                await join_voice_channel(voice_channel)

async def join_voice_channel(voice_channel):
    global CONNECT
    CONNECT = True
    if voice_channel.guild.voice_client is None:
        await voice_channel.connect()
        print(f'Joined voice channel: {voice_channel.name}')
        await play_audio(voice_channel, "LauDaiTinhAi.opus")

client.run(TOKEN)