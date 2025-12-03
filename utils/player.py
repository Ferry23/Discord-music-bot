import discord
import yt_dlp  # type: ignore
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
        self.skip_votes = set()
        self.auto_related = True

    def create_audio_source(self, url):
        try:
            import shutil
            ffmpeg_path = shutil.which('ffmpeg')
            if ffmpeg_path:
                logging.info(f"Found FFmpeg at: {ffmpeg_path}")
                # Use FFmpeg with the extracted URL
                return discord.FFmpegPCMAudio(url,
                    executable=ffmpeg_path,
                    before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    options='-vn -f s16le -ar 48000 -ac 2')
            else:
                logging.warning("FFmpeg not found in PATH, trying default")
                return discord.FFmpegPCMAudio(url,
                    before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    options='-vn')
        except Exception as e:
            logging.error(f"Error creating audio source: {e}")
            return None

    async def play_next(self):
        logging.info(f"Play next called. Queue size: {self.queue.size()}, is_playing: {self.is_playing}")

        if self.queue.is_empty():
            logging.info("Queue is empty")
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

        logging.info(f"Attempting to play: {track['title']} - URL: {track['url'][:50]}...")

        try:
            source = self.create_audio_source(track['url'])
            if source is None:
                logging.error("Failed to create audio source")
                self.is_playing = False
                self.current_track = None
                asyncio.create_task(self.play_next())
                return

            if hasattr(source, 'volume'):
                source.volume = self.volume
            self.voice_client.play(source, after=self.after_play)
            logging.info(f"Now playing: {track['title']}")
        except Exception as e:
            logging.error(f"Error playing track: {e}")
            self.is_playing = False
            self.current_track = None
            # Try next track
            asyncio.create_task(self.play_next())

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


    def vote_skip(self, member):
        if member.id in self.skip_votes:
            return False
        self.skip_votes.add(member.id)
        return True

    def should_skip_vote(self, total_members):
        return len(self.skip_votes) >= int(total_members * Config.VOTE_SKIP_THRESHOLD)