import discord
import yt_dlp
import asyncio
import logging
from config.config import Config
from utils.search import MusicSearch

class MusicPlayer:
    def __init__(self, voice_client, queue):
        self.voice_client = voice_client
        self.queue = queue
        self.current_track = None
        self.is_playing = False
        self.idle_task = None
        self.volume = Config.DEFAULT_VOLUME / 100.0
        self.stay_247 = False
        self.dj_role_id = None
        self.skip_votes = set()
        self.auto_related = True

    def create_audio_source(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '-',
            'quiet': True,
            'no_warnings': True,
        }
        return discord.FFmpegPCMAudio(url, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', options='-vn')

    async def play_next(self):
        if self.queue.is_empty():
            if self.auto_related and self.current_track:
                # Add related songs
                related_query = f"{self.current_track['title']} related songs"
                related_track = MusicSearch.search(related_query)
                if related_track:
                    self.queue.add_track(related_track)
                    logging.info(f"Added related song: {related_track['title']}")
                else:
                    if not self.stay_247:
                        await self.start_idle_timer()
                    return
            else:
                if not self.stay_247:
                    await self.start_idle_timer()
                return

        track = self.queue.get_next()
        self.current_track = track
        self.is_playing = True
        self.skip_votes.clear()

        source = self.create_audio_source(track['url'])
        if hasattr(source, 'volume'):
            source.volume = self.volume
        self.voice_client.play(source, after=self.after_play)

        logging.info(f"Now playing: {track['title']}")

    def after_play(self, error):
        if error:
            logging.error(f"Playback error: {error}")
        self.is_playing = False
        self.current_track = None
        asyncio.run_coroutine_threadsafe(self.play_next(), self.voice_client.loop)

    async def pause(self):
        if self.voice_client.is_playing():
            self.voice_client.pause()

    async def resume(self):
        if self.voice_client.is_paused():
            self.voice_client.resume()

    async def stop(self):
        self.voice_client.stop()
        self.is_playing = False
        self.current_track = None
        self.queue.clear()

    async def start_idle_timer(self):
        if self.idle_task:
            self.idle_task.cancel()
        if not self.stay_247:
            self.idle_task = asyncio.create_task(self.idle_disconnect())

    async def idle_disconnect(self):
        await asyncio.sleep(Config.IDLE_TIMEOUT)
        if not self.is_playing and self.queue.is_empty():
            await self.voice_client.disconnect()
            logging.info("Disconnected due to idle timeout")

    def cancel_idle_timer(self):
        if self.idle_task:
            self.idle_task.cancel()
            self.idle_task = None

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume / 100.0))
        if self.voice_client.source:
            self.voice_client.source.volume = self.volume

    def toggle_stay(self):
        self.stay_247 = not self.stay_247
        if self.stay_247:
            self.cancel_idle_timer()
        else:
            if not self.is_playing and self.queue.is_empty():
                asyncio.create_task(self.start_idle_timer())

    def set_dj_role(self, role_id):
        self.dj_role_id = role_id

    def can_skip(self, member):
        if self.dj_role_id:
            return any(role.id == self.dj_role_id for role in member.roles)
        return True

    def vote_skip(self, member):
        if member.id in self.skip_votes:
            return False
        self.skip_votes.add(member.id)
        return True

    def should_skip_vote(self, total_members):
        return len(self.skip_votes) >= int(total_members * Config.VOTE_SKIP_THRESHOLD)