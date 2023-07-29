import discord
from secret import TOKEN, CHANNEL_NAME, GUILD_NAME
from discord.ext import commands
import asyncio
from discord.opus import load

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def create_or_get_channel(guild, channel_name):
    existing_channel = discord.utils.get(guild.voice_channels, name=channel_name)
    
    if existing_channel:
        return existing_channel

    new_channel = await guild.create_voice_channel(name=channel_name)
    return new_channel

@client.event
async def on_ready():
    global GUILD_INFO
    GUILD_INFO = {}

    for guild in client.guilds:
        GUILD_INFO[guild.id] = {
            'guild': guild,
            'channel': await create_or_get_channel(guild, CHANNEL_NAME)
        }
        print(f"Channel '{GUILD_INFO[guild.id]['channel'].name}' with ID '{GUILD_INFO[guild.id]['channel'].id}' created/obtained for Guild '{guild.name}' with ID '{guild.id}'.")
    print(f"Bot is ready. Logged in as {client.user}.")

async def disconnect_if_empty(voice_channel):
    await asyncio.sleep(15)  # Wait for 15 seconds
    if len(voice_channel.members) == 1:  # Only the bot is present in the channel
        await voice_channel.guild.voice_client.disconnect()
        print(f'Disconnected from voice channel: {voice_channel.name}')

async def play_audio(voice_channel):
    audio_file = "LauDaiTinhAi.opus"
    voice_client = voice_channel.guild.voice_client

    if voice_client.is_playing():
        voice_client.stop()

    audio_source = discord.FFmpegPCMAudio(audio_file)
    voice_client.play(audio_source, after=lambda e: print(f"Finished playing: {audio_file}"))

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
        await play_audio(voice_channel)

client.run(TOKEN)


