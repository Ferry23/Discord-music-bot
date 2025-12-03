import discord
from discord.ext import commands
import time
from utils.embed_builder import EmbedBuilder

class UtilsCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: {latency}ms", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(title="🤖 Bot Info", color=0x3498db)
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=len(self.bot.users), inline=True)
        embed.add_field(name="Commands", value=len(self.bot.commands), inline=True)
        embed.add_field(name="Python Version", value="3.8+", inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        uptime_seconds = int(time.time() - self.start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours}h {minutes}m {seconds}s"
        embed = discord.Embed(title="⏰ Uptime", description=uptime_str, color=0xe67e22)
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        embed = EmbedBuilder.help_embed()
        await ctx.send(embed=embed)

    @commands.command()
    async def ffmpegtest(self, ctx):
        """Test FFmpeg availability"""
        import subprocess
        import shutil
        import os

        response = "**FFmpeg Test Results:**\n\n"

        # Check PATH
        ffmpeg_in_path = shutil.which('ffmpeg')
        response += f"FFmpeg in PATH: `{ffmpeg_in_path or 'Not found'}`\n"

        # Check environment variable
        ffmpeg_env = os.environ.get('FFMPEG_PATH')
        response += f"FFMPEG_PATH env: `{ffmpeg_env or 'Not set'}`\n"

        # Test execution
        try:
            if ffmpeg_in_path or ffmpeg_env:
                test_path = ffmpeg_env or ffmpeg_in_path
                result = subprocess.run([test_path, '-version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version_line = result.stdout.split('\n')[0] if result.stdout else 'Unknown version'
                    response += f"FFmpeg test: ✅ Working\nVersion: `{version_line}`"
                else:
                    response += f"FFmpeg test: ❌ Failed (exit code {result.returncode})"
            else:
                response += "FFmpeg test: ❌ Not found in PATH or env"
        except Exception as e:
            response += f"FFmpeg test: ❌ Exception - {e}"

        await ctx.send(response)


async def setup(bot):
    await bot.add_cog(UtilsCommandsCog(bot))