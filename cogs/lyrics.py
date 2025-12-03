import discord
from discord.ext import commands
import lyricsgenius
from config.config import Config
from utils.embed_builder import EmbedBuilder

class LyricsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.genius = lyricsgenius.Genius(Config.GENIUS_ACCESS_TOKEN)

    @commands.command()
    async def lirik(self, ctx, *, query=None):
        if not query:
            # Get from current track
            player = self.bot.get_cog('MusicCog').get_player(ctx.guild)
            if player and player.current_track:
                query = player.current_track['title']
            else:
                await ctx.send("No song is playing. Please provide a song title.")
                return

        try:
            song = self.genius.search_song(query)
            if song:
                embed = EmbedBuilder.lyrics_embed(song.title, song.lyrics)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Lyrics not found.")
        except Exception as e:
            await ctx.send("Error fetching lyrics.")
            print(e)

async def setup(bot):
    await bot.add_cog(LyricsCog(bot))