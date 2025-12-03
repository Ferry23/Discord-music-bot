import yt_dlp
from youtubesearchpython import VideosSearch
import re
import logging

class MusicSearch:
    @staticmethod
    def is_youtube_url(url):
        return re.match(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/', url)

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
        try:
            videos_search = VideosSearch(query, limit=1)
            result = videos_search.result()
            if result['result']:
                video = result['result'][0]
                return {
                    'url': f"https://www.youtube.com/watch?v={video['id']}",
                    'title': video['title'],
                    'duration': video['duration'],
                    'thumbnail': video['thumbnails'][0]['url'] if video['thumbnails'] else None
                }
        except Exception as e:
            logging.error(f"Error searching YouTube: {e}")
        return None

    @staticmethod
    def get_video_info(url):
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'url': info['url'],
                    'title': info['title'],
                    'duration': info['duration'],
                    'thumbnail': info['thumbnail']
                }
        except Exception as e:
            logging.error(f"Error extracting video info: {e}")
        return None

    @classmethod
    def search(cls, query_or_url):
        if cls.is_youtube_url(query_or_url) or cls.is_soundcloud_url(query_or_url):
            return cls.get_video_info(query_or_url)
        elif cls.is_spotify_url(query_or_url):
            # For Spotify, try to get title from URL or assume it's a search
            # Simplified: treat as search query
            # In advanced, use spotipy to get track info
            return cls.search_youtube(query_or_url)  # Placeholder
        else:
            return cls.search_youtube(query_or_url)