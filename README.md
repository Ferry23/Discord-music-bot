# Discord Music Bot

Bot musik Discord dengan fitur modern:
- Streaming dari YouTube, Spotify, SoundCloud
- Queue lengkap (skip, pause, resume, shuffle, repeat)
- Auto-related songs
- Playlist custom per server
- Now Playing embed yang rapi
- Fitur lirik dari Genius API
- DJ mode & skip voting
- History & auto disconnect

## Instalasi

1. Clone repository
git clone <repo>
cd Bot-musik

2. Install dependensi:
pip install -r requirements.txt

3. Buat file config:
config/config.py

4. Isi:
DISCORD_TOKEN = "TOKEN_BOT_DISCORD_ANDA"
GENIUS_ACCESS_TOKEN = "TOKEN_GENIUS"

5. Jalankan bot:
python bot.py


## Cara Menggunakan

- !play <judul/link>
- !lirik
- !queue
- !skip
- !playlist create <nama>
- !playlist add <nama> <lagu>
- !playlist play <nama>

## Catatan

Pastikan FFmpeg sudah terinstal di komputer Anda.