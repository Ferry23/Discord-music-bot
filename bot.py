import discord
from discord.ext import commands
import logging
import os
from config.config import Config

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Validate config
Config.validate()

# Set FFmpeg path for audio processing
if not os.environ.get('FFMPEG_PATH'):
    # Try to find FFmpeg in common locations (Windows & Linux)
    ffmpeg_paths = [
        # Windows paths
        r'C:\ProgramData\chocolatey\bin\ffmpeg.exe',
        r'C:\ProgramData\Chocolatey\bin\ffmpeg.exe',
        r'C:\path_programs\ffmpeg.exe',
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\FFmpeg\bin\ffmpeg.exe',
        # Linux paths (Railway, etc.)
        '/usr/bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        '/bin/ffmpeg',
        '/opt/ffmpeg/bin/ffmpeg',
        '/app/ffmpeg/ffmpeg',
        '/nix/store/*/bin/ffmpeg'
    ]
    for path in ffmpeg_paths:
        if os.path.exists(path):
            os.environ['FFMPEG_PATH'] = path
            logging.info(f"Set FFMPEG_PATH to: {path}")
            break

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=Config.COMMAND_PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    logging.info(f'Bot is ready. Logged in as {bot.user}')

# Load cogs
async def load_cogs():
    await bot.load_extension('cogs.music')
    await bot.load_extension('cogs.lyrics')
    await bot.load_extension('cogs.playlist')
    await bot.load_extension('cogs.utils_commands')
    logging.info('Cogs loaded successfully')

async def main():
    await load_cogs()
    await bot.start(Config.DISCORD_TOKEN)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())