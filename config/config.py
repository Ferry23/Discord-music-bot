import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    GENIUS_ACCESS_TOKEN = os.getenv('GENIUS_ACCESS_TOKEN')
    COMMAND_PREFIX = '!'
    IDLE_TIMEOUT = 300  # 5 minutes in seconds
    DEFAULT_VOLUME = 50  # 0-100
    MAX_QUEUE_SIZE = 100
    VOTE_SKIP_THRESHOLD = 0.5  # 50%

    @classmethod
    def validate(cls):
        if not cls.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN environment variable is not set")
        if not cls.GENIUS_ACCESS_TOKEN:
            raise ValueError("GENIUS_ACCESS_TOKEN environment variable is not set")