# 🎵 Discord Music Bot

**✅ BOT SUDAH BERFUNGSI LENGKAP!**

Bot musik Discord lengkap dengan fitur-fitur modern dan advanced! Mendukung streaming musik dari berbagai platform dengan antarmuka yang user-friendly.

**Status**: 🟢 **Fully Functional** - Semua fitur telah ditest dan bekerja dengan baik!

## ✨ Fitur Utama

### 🎶 Musik Streaming
- **Multi-platform support**: YouTube, Spotify (converted to YouTube)
- **Streaming langsung**: Tidak download file, hemat storage
- **High quality audio**: Menggunakan yt-dlp + FFmpeg

### 📋 Queue Management
- **Queue lengkap**: Add, remove, view dengan pagination
- **Shuffle & Repeat**: Mode shuffle dan repeat (off/one/all)
- **History**: Riwayat lagu yang pernah diputar
- **Auto-related**: Otomatis add lagu terkait jika queue kosong

### 📝 Playlist Custom
- **Server playlists**: Playlist per server yang persistent
- **CRUD operations**: Create, add, play, list, delete playlist
- **JSON storage**: Data tersimpan dalam file JSON

### 🎤 Advanced Features
- **Now Playing**: Embed rapi dengan progress bar
- **Lyrics**: Ambil lirik dari Genius API
- **Volume control**: Atur volume 1-100%
- **24/7 Mode**: Bot tetap online di voice channel
- **24/7 Mode**: Bot tetap online di voice channel
- **Auto disconnect**: Disconnect otomatis setelah idle 5 menit

### 🤖 Bot Features
- **Multi-cog architecture**: Modular dan maintainable
- **Error handling**: Pesan error yang user-friendly
- **Logging**: Comprehensive logging untuk debugging
- **Embed UI**: Interface yang cantik dengan Discord embeds

## 🚀 Quick Start

### Persiapan
1. **Clone repository**:
   ```bash
   git clone https://github.com/Ferry23/Discord-music-bot.git
   cd Discord-music-bot
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg** (wajib untuk audio streaming):
   - **Windows**: Download dari [ffmpeg.org](https://ffmpeg.org/download.html) dan tambahkan ke PATH
   - **Linux**: `sudo apt install ffmpeg`
   - **Mac**: `brew install ffmpeg`

### Setup Bot Token

1. **Buat Discord Bot**:
   - Kunjungi [Discord Developer Portal](https://discord.com/developers/applications)
   - Buat aplikasi baru → Bot → Copy token

2. **Dapatkan Genius API Token**:
   - Kunjungi [Genius API](https://genius.com/api-clients)
   - Buat app baru → Copy access token

3. **Setup Environment**:
   ```bash
   # Copy template
   cp .env.example .env

   # Edit .env dan isi token
   DISCORD_TOKEN=your_discord_bot_token_here
   GENIUS_ACCESS_TOKEN=your_genius_access_token_here
   ```

### Menjalankan Bot
```bash
python bot.py
```

Bot akan online dan siap digunakan!

## 📖 Cara Penggunaan

### Command Musik Dasar
```
!play <judul/link>    - Putar musik dari YouTube/Spotify/SoundCloud
!skip                 - Skip lagu saat ini
!pause                - Pause musik
!resume               - Resume musik
!stop                 - Stop musik dan clear queue
!nowplaying           - Lihat lagu yang sedang diputar
```

### Queue Management
```
!queue [page]         - Lihat queue (dengan pagination)
!volume <1-100>       - Atur volume bot
!shuffle              - Shuffle queue
!repeat <off/one/all> - Set mode repeat
!history              - Lihat riwayat lagu
```

### Playlist Commands
```
!playlist create <nama>     - Buat playlist baru
!playlist add <nama> <lagu> - Tambah lagu ke playlist
!playlist play <nama>       - Putar seluruh playlist
!playlist list              - Lihat semua playlist server
!playlist show <nama>       - Lihat isi playlist
!playlist delete <nama>     - Hapus playlist
```

### Fitur Tambahan
```
!lirik [judul]        - Lihat lirik lagu (otomatis dari lagu yang diputar)
!dj <@role>           - Set DJ role (hanya role ini yang bisa skip/stop)
!stay                 - Toggle 24/7 mode
!ping                 - Check latency bot
!botinfo              - Info bot
!uptime               - Waktu bot online
```


## 🏗️ Struktur Proyek

```
Discord-music-bot/
├── bot.py                    # Entry point utama
├── config/
│   └── config.py            # Konfigurasi bot
├── cogs/
│   ├── music.py             # Commands musik utama
│   ├── lyrics.py            # Commands lirik
│   ├── playlist.py          # Commands playlist
│   └── utils_commands.py    # Commands utilitas
├── utils/
│   ├── player.py            # Logic audio player
│   ├── queue.py             # Management queue
│   ├── search.py            # Pencarian musik
│   ├── embed_builder.py     # Builder embed UI
│   └── storage.py           # Load/save data JSON
├── data/
│   ├── playlists.json       # Storage playlist server
│   └── history.json         # Storage riwayat lagu
├── requirements.txt         # Python dependencies
├── .env.example            # Template environment variables
├── .gitignore              # Git ignore rules
└── README.md               # File ini
```

## 🔧 Konfigurasi

Edit `config/config.py` untuk customize:
- `COMMAND_PREFIX`: Prefix command (default: '!')
- `IDLE_TIMEOUT`: Waktu idle sebelum disconnect (detik)
- `DEFAULT_VOLUME`: Volume default (0-100)
- `MAX_QUEUE_SIZE`: Max lagu dalam queue
- `VOTE_SKIP_THRESHOLD`: Threshold voting skip (0.0-1.0)

## 🛠️ Troubleshooting

### Bot tidak bisa join voice channel
- Pastikan bot punya permission: `Connect`, `Speak`, `Use Voice Activity`
- Invite ulang bot dengan permissions yang benar

### Tidak ada audio
- Pastikan FFmpeg terinstall dengan benar
- Check log bot untuk error messages

### Token error
- Pastikan `.env` file ada dan token benar
- Jangan commit `.env` ke GitHub (sudah di-ignore)

### Dependencies error
- Install ulang: `pip install -r requirements.txt`
- Pastikan Python 3.8+

## 📝 Contributing

1. Fork repository
2. Buat branch feature baru: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add some AmazingFeature'`
4. Push ke branch: `git push origin feature/AmazingFeature`
5. Buat Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👨‍💻 Author

**Ferry Ardiansyah** - [GitHub](https://github.com/Ferry23)

## 🙏 Acknowledgments

- [discord.py](https://discordpy.readthedocs.io/) - Discord API wrapper
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [lyricsgenius](https://github.com/johnwmillr/lyricsgenius) - Genius API wrapper
- [FFmpeg](https://ffmpeg.org/) - Audio processing

---

**Enjoy your music! 🎵**