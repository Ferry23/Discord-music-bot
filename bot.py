import discord
from discord.ext import commands
import logging
from config.config import Config

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Validate config
Config.validate()

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