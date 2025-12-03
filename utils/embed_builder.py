import discord
from datetime import timedelta

class EmbedBuilder:
    @staticmethod
    def now_playing(track, requester, volume, repeat_mode, shuffled):
        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{track['title']}**",
            color=0x00ff00
        )
        embed.set_thumbnail(url=track.get('thumbnail', ''))
        embed.add_field(name="Duration", value=str(timedelta(seconds=track.get('duration', 0))), inline=True)
        embed.add_field(name="Requested by", value=requester.mention, inline=True)
        embed.add_field(name="Volume", value=f"{int(volume * 100)}%", inline=True)
        embed.add_field(name="Repeat", value=repeat_mode.title(), inline=True)
        embed.add_field(name="Shuffle", value="On" if shuffled else "Off", inline=True)
        # Progress bar placeholder
        embed.add_field(name="Progress", value="▬▬▬▬▬▬▬▬▬▬ 0:00 / " + str(timedelta(seconds=track.get('duration', 0))), inline=False)
        return embed

    @staticmethod
    def queue_list(queue, page=1, per_page=10):
        embed = discord.Embed(
            title="🎶 Queue",
            color=0x3498db
        )
        if not queue:
            embed.description = "Queue is empty"
            return embed

        start = (page - 1) * per_page
        end = start + per_page
        queue_slice = queue[start:end]

        description = ""
        for i, track in enumerate(queue_slice, start + 1):
            description += f"{i}. {track['title']} - {str(timedelta(seconds=track.get('duration', 0)))}\n"

        embed.description = description
        embed.set_footer(text=f"Page {page} | Total: {len(queue)}")
        return embed

    @staticmethod
    def help_embed():
        embed = discord.Embed(
            title="🎵 Music Bot Help",
            description="Berikut adalah cara penggunaan bot musik ini:",
            color=0xe67e22
        )
        embed.add_field(
            name="🎶 Perintah Musik",
            value="`!play <lagu/link>` - Putar lagu\n`!queue [halaman]` - Lihat antrian\n`!skip` - Lewati lagu\n`!pause` - Jeda\n`!resume` - Lanjutkan\n`!stop` - Hentikan dan hapus antrian\n`!volume <1-100>` - Atur volume\n`!shuffle` - Acak antrian\n`!repeat <off/one/all>` - Set ulang\n`!nowplaying` - Lihat lagu yang sedang diputar\n`!history` - Riwayat lagu\n`!stay` - Mode 24/7",
            inline=False
        )
        embed.add_field(
            name="📋 Perintah Playlist",
            value="`!playlist create <nama>` - Buat playlist\n`!playlist add <nama> <lagu>` - Tambah lagu ke playlist\n`!playlist play <nama>` - Putar playlist\n`!playlist list` - Lihat semua playlist\n`!playlist show <nama>` - Lihat isi playlist\n`!playlist delete <nama>` - Hapus playlist",
            inline=False
        )
        embed.add_field(
            name="📝 Perintah Lain",
            value="`!lirik [lagu]` - Cari lirik (jika tidak ada, dari lagu sekarang)\n`!ping` - Cek latency bot\n`!botinfo` - Info bot\n`!uptime` - Waktu aktif bot\n`!help` - Tampilkan bantuan ini",
            inline=False
        )
        embed.set_footer(text="Bot musik Discord - Gunakan prefix !")
        return embed

    @staticmethod
    def lyrics_embed(title, lyrics):
        embed = discord.Embed(
            title=f"📝 Lyrics: {title}",
            description=lyrics[:2000],
            color=0x9b59b6
        )
        return embed

    @staticmethod
    def playlist_embed(name, tracks):
        embed = discord.Embed(
            title=f"📋 Playlist: {name}",
            color=0xf1c40f
        )
        if tracks:
            description = "\n".join([f"{i+1}. {track['title']}" for i, track in enumerate(tracks)])
            embed.description = description
        else:
            embed.description = "Empty playlist"
        return embed

    @staticmethod
    def history_embed(history):
        embed = discord.Embed(
            title="📜 Recently Played",
            color=0x95a5a6
        )
        if history:
            description = "\n".join([f"{i+1}. {track['title']}" for i, track in enumerate(history[-10:])])
            embed.description = description
        else:
            embed.description = "No history"
        return embed