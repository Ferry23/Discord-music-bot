import discord
from discord.ext import commands
import logging
from utils.search import MusicSearch
from utils.queue import MusicQueue
from utils.player import MusicPlayer
from utils.embed_builder import EmbedBuilder
from utils.storage import Storage

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.last_channel = {}  # guild_id -> channel

    def get_player(self, guild):
        if guild.id not in self.players:
            voice_client = guild.voice_client
            if not voice_client:
                return None
            queue = MusicQueue()
            self.players[guild.id] = MusicPlayer(voice_client, queue)
        return self.players[guild.id]

    @commands.command()
    async def play(self, ctx, *, query):
        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel!")
            return

        voice_channel = ctx.author.voice.channel
        if not ctx.guild.voice_client:
            await voice_channel.connect()

        # Store the channel for auto Now Playing messages
        self.last_channel[ctx.guild.id] = ctx.channel

        player = self.get_player(ctx.guild)
        if not player:
            return

        track = MusicSearch.search(query)
        if not track:
            await ctx.send("Could not find the track.")
            return

        player.queue.add_track(track)
        await ctx.send(f"Added to queue: {track['title']}")

        if not player.is_playing:
            player.cancel_idle_timer()
            await player.play_next(ctx)  # Pass ctx for Now Playing

    @commands.command()
    async def queue(self, ctx, page: int = 1):
        player = self.get_player(ctx.guild)
        if not player or player.queue.is_empty():
            await ctx.send("Queue is empty.")
            return

        queue_list = player.queue.get_queue()
        embed = EmbedBuilder.queue_list(queue_list, page)
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        player = self.get_player(ctx.guild)
        if not player or not player.is_playing:
            await ctx.send("No track is playing.")
            return

        # Anyone can skip directly
        player.voice_client.stop()
        await ctx.send("Skipped current track.")

    @commands.command()
    async def pause(self, ctx):
        player = self.get_player(ctx.guild)
        if player:
            await player.pause()
            await ctx.send("Paused.")

    @commands.command()
    async def resume(self, ctx):
        player = self.get_player(ctx.guild)
        if player:
            await player.resume()
            await ctx.send("Resumed.")

    @commands.command()
    async def stop(self, ctx):
        player = self.get_player(ctx.guild)
        if player:
            await player.stop()
            await ctx.send("Stopped and cleared queue.")

    @commands.command()
    async def volume(self, ctx, vol: int):
        player = self.get_player(ctx.guild)
        if player:
            player.set_volume(vol)
            await ctx.send(f"Volume set to {vol}%")

    @commands.command()
    async def shuffle(self, ctx):
        player = self.get_player(ctx.guild)
        if player:
            player.queue.shuffle()
            await ctx.send("Queue shuffled.")

    @commands.command()
    async def repeat(self, ctx, mode: str):
        player = self.get_player(ctx.guild)
        if player and mode in ['off', 'one', 'all']:
            player.queue.set_repeat(mode)
            await ctx.send(f"Repeat set to {mode}")

    @commands.command()
    async def nowplaying(self, ctx):
        player = self.get_player(ctx.guild)
        if player and player.current_track:
            embed = EmbedBuilder.now_playing(
                player.current_track, ctx.author,
                player.volume, player.queue.repeat_mode, player.queue.shuffled
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No track is playing.")

    @commands.command()
    async def history(self, ctx):
        history = Storage.load_history()
        embed = EmbedBuilder.history_embed(history)
        await ctx.send(embed=embed)

    @commands.command()
    async def stay(self, ctx):
        player = self.get_player(ctx.guild)
        if player:
            player.toggle_stay()
            status = "enabled" if player.stay_247 else "disabled"
            await ctx.send(f"24/7 mode {status}")


async def setup(bot):
    await bot.add_cog(MusicCog(bot))