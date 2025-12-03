import discord
from discord.ext import commands
from utils.search import MusicSearch
from utils.storage import Storage
from utils.embed_builder import EmbedBuilder

class PlaylistCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def playlist(self, ctx):
        await ctx.send("Use `!playlist create <name>`, `!playlist add <name> <song>`, `!playlist play <name>`, etc.")

    @playlist.command()
    async def create(self, ctx, name: str):
        playlists = Storage.load_playlists()
        guild_id = str(ctx.guild.id)
        if guild_id not in playlists:
            playlists[guild_id] = {}
        if name in playlists[guild_id]:
            await ctx.send(f"Playlist '{name}' already exists.")
            return
        playlists[guild_id][name] = []
        Storage.save_playlists(playlists)
        await ctx.send(f"Playlist '{name}' created.")

    @playlist.command()
    async def add(self, ctx, name: str, *, query: str):
        playlists = Storage.load_playlists()
        guild_id = str(ctx.guild.id)
        if guild_id not in playlists or name not in playlists[guild_id]:
            await ctx.send(f"Playlist '{name}' does not exist.")
            return
        track = MusicSearch.search(query)
        if not track:
            await ctx.send("Track not found.")
            return
        playlists[guild_id][name].append(track)
        Storage.save_playlists(playlists)
        await ctx.send(f"Added '{track['title']}' to playlist '{name}'.")

    @playlist.command()
    async def play(self, ctx, name: str):
        playlists = Storage.load_playlists()
        guild_id = str(ctx.guild.id)
        if guild_id not in playlists or name not in playlists[guild_id]:
            await ctx.send(f"Playlist '{name}' does not exist.")
            return
        tracks = playlists[guild_id][name]
        if not tracks:
            await ctx.send(f"Playlist '{name}' is empty.")
            return

        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel!")
            return

        voice_channel = ctx.author.voice.channel
        if not ctx.guild.voice_client:
            await voice_channel.connect()

        # Store the channel for auto Now Playing messages
        music_cog = self.bot.get_cog('MusicCog')
        music_cog.last_channel[ctx.guild.id] = ctx.channel

        player = music_cog.get_player(ctx.guild)
        if not player:
            return

        for track in tracks:
            player.queue.add_track(track)

        await ctx.send(f"Added playlist '{name}' to queue.")

        if not player.is_playing:
            player.cancel_idle_timer()
            await player.play_next(ctx)  # Pass ctx for Now Playing

    @playlist.command()
    async def list(self, ctx):
        playlists = Storage.load_playlists()
        guild_id = str(ctx.guild.id)
        if guild_id not in playlists or not playlists[guild_id]:
            await ctx.send("No playlists found.")
            return
        embed = discord.Embed(title="Playlists", color=0xf1c40f)
        for name, tracks in playlists[guild_id].items():
            embed.add_field(name=name, value=f"{len(tracks)} tracks", inline=True)
        await ctx.send(embed=embed)

    @playlist.command()
    async def show(self, ctx, name: str):
        playlists = Storage.load_playlists()
        guild_id = str(ctx.guild.id)
        if guild_id not in playlists or name not in playlists[guild_id]:
            await ctx.send(f"Playlist '{name}' does not exist.")
            return
        tracks = playlists[guild_id][name]
        embed = EmbedBuilder.playlist_embed(name, tracks)
        await ctx.send(embed=embed)

    @playlist.command()
    async def delete(self, ctx, name: str):
        playlists = Storage.load_playlists()
        guild_id = str(ctx.guild.id)
        if guild_id not in playlists or name not in playlists[guild_id]:
            await ctx.send(f"Playlist '{name}' does not exist.")
            return
        del playlists[guild_id][name]
        Storage.save_playlists(playlists)
        await ctx.send(f"Playlist '{name}' deleted.")

async def setup(bot):
    await bot.add_cog(PlaylistCog(bot))