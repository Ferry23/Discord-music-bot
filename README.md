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

3. Setup environment variables:
- Copy .env.example ke .env
- Isi token-token Anda:
```
DISCORD_TOKEN=your_discord_bot_token_here
GENIUS_ACCESS_TOKEN=your_genius_access_token_here
```

4. Jalankan bot:
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