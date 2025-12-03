import yt_dlp  # type: ignore
from youtubesearchpython import VideosSearch  # type: ignore
import re
import logging

class MusicSearch:
    @staticmethod
    def is_youtube_url(url):
        return re.match(r'(https?://)?(www\.|music\.)?(youtube\.com|youtu\.be)/', url)

    @staticmethod
    def is_spotify_url(url):
        return re.match(r'(https?://)?(open\.spotify\.com)/', url)

    @staticmethod
    def is_soundcloud_url(url):
        return re.match(r'(https?://)?(soundcloud\.com)/', url)

    @staticmethod
    def extract_spotify_info(url):
        # Simple extraction, in real app might need better parsing
        # For simplicity, assume it's a track and extract from yt-dlp if possible
        # But yt-dlp can handle Spotify with cookies, but for now, return None and handle as search
        return None

    @staticmethod
    def search_youtube(query):
        # Use yt-dlp search directly (more reliable)
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'default_search': 'ytsearch1',
                'noplaylist': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)
                if info and 'entries' in info and info['entries']:
                    entry = info['entries'][0]
                    return {
                        'url': entry.get('url', entry.get('webpage_url', '')),
                        'title': entry.get('title', 'Unknown Title'),
                        'duration': entry.get('duration', 0),
                        'thumbnail': entry.get('thumbnail', '')
                    }
        except Exception as e:
            logging.error(f"YouTube search failed: {e}")
        return None

    @staticmethod
    def get_video_info(url):
        # Clean URL from playlist parameters to avoid playlist extraction
        if 'youtube.com' in url or 'youtu.be' in url:
            url = url.split('&')[0]  # Remove playlist and other parameters

        # Different options for different platforms
        if 'soundcloud.com' in url:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'noplaylist': True,
                'format': 'bestaudio[abr<=128]/best[abr<=128]',  # SoundCloud specific format
                'ffmpeg_location': None,
                'postprocessors': [],
            }
        else:
            # YouTube and others
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'noplaylist': True,
                'format': 'bestaudio[abr<=128]/best[abr<=128]',  # General audio format
                'ffmpeg_location': None,
                'postprocessors': [],
            }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                # For audio, we need the actual stream URL
                # yt-dlp should give us the direct URL after extraction
                if 'url' in info and info['url']:
                    video_url = info['url']
                elif 'formats' in info and info['formats']:
                    # Find best audio format
                    audio_formats = [f for f in info['formats'] if f.get('acodec') != 'none']
                    if audio_formats:
                        # Sort by quality (prefer higher bitrate)
                        audio_formats.sort(key=lambda x: x.get('abr', 0), reverse=True)
                        video_url = audio_formats[0].get('url', '')
                    else:
                        # Fallback to first format
                        video_url = info['formats'][0].get('url', '')
                else:
                    logging.error(f"No URL found in info dict: {list(info.keys())}")
                    return None

                if not video_url:
                    logging.error("Empty video URL extracted")
                    return None

                logging.info(f"Extracted URL: {video_url[:100]}...")

                return {
                    'url': video_url,
                    'title': info.get('title', 'Unknown Title'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', '')
                }
        except Exception as e:
            logging.error(f"Error extracting video info: {e}")
        return None

    @classmethod
    def search(cls, query_or_url):
        logging.info(f"Searching for: {query_or_url}")

        if cls.is_youtube_url(query_or_url):
            logging.info("Detected YouTube URL")
            return cls.get_video_info(query_or_url)
        elif cls.is_soundcloud_url(query_or_url):
            logging.info("Detected SoundCloud URL")
            return cls.get_video_info(query_or_url)
        elif cls.is_spotify_url(query_or_url):
            logging.info("Detected Spotify URL")
            # For Spotify, treat as search query then extract full info
            search_result = cls.search_youtube(query_or_url)
            if search_result and search_result['url']:
                return cls.get_video_info(search_result['url'])
            return search_result
        else:
            logging.info("Detected search query")
            # For search queries, search then extract full info
            search_result = cls.search_youtube(query_or_url)
            if search_result and search_result['url']:
                return cls.get_video_info(search_result['url'])
            return search_result