import asyncio
import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import yt_dlp as youtube_dl
import spotipy
from typing import Dict
from .components.music import Music
from .utils.loadData import load_json


FFMPEG_PATH = os.getenv('FFMPEG_PATH')
YT_DL_OPTIONS = {
    "format": "bestaudio/best"
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=0.15"'
}

class PlaySong(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ytdl = youtube_dl.YoutubeDL(YT_DL_OPTIONS)
        self.guilds_music: Dict[str, Music] = {}
        self.recommended_songs = load_json('docs/songs.json')["recommended_songs"]

    # play command
    @app_commands.command(name = "play", description = "播放音樂")
    @app_commands.describe(url = "音樂連結")
    async def sing(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer()
        
        if not await self.play_song(interaction, url):
            await interaction.followup.send("無法播放此音樂")

        await interaction.followup.send("音樂已加入播放清單")
    
    # auto play command
    @app_commands.command(name = "auto", description = "自動播放音樂")
    async def auto_play(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.guild_id not in self.guilds_music.keys():
            if not await self.play_song(interaction, 'https://www.youtube.com/watch?v=' + random.choice(self.recommended_songs)):
                await interaction.followup.send("無法播音樂")
                return

        guild_music = self.guilds_music[interaction.guild_id]
        guild_music.set_auto_play(not guild_music.get_auto_play())
        await interaction.followup.send("自動播放已" + ("開啟" if guild_music.get_auto_play() else "關閉"))


    # function command
    @app_commands.command(name = "control", description = "控制音樂撥放")
    @app_commands.describe(method = "操作方式")
    @app_commands.choices(
        method = [
            Choice(name = "暫停", value = "pause"),
            Choice(name = "繼續", value = "resume"),
            Choice(name = "下一首", value = "skip"),
            Choice(name = "停止", value = "stop"),
        ]
    )
    async def control(self, interaction: discord.Interaction, method: str):
        if interaction.guild_id not in self.guilds_music.keys():
            await interaction.response.send_message("目前沒有音樂在播放")
            return

        await interaction.response.defer()
        try:
            guild_music = self.guilds_music[interaction.guild_id]
            voice_client = guild_music.get_voice_client()
            if method == "pause":
                voice_client.pause()
                await interaction.followup.send("音樂暫停")
            elif method == "resume":
                voice_client.resume()
                await interaction.followup.send("音樂繼續")
            elif method == "skip":
                await voice_client.stop()
                await self.play_next(interaction)
                await interaction.followup.send("已跳過此首音樂")
            elif method == "stop":
                guild_music.set_playing(False)
                voice_client.stop()
                await voice_client.disconnect()
                del self.guilds_music[interaction.guild_id]
                await interaction.followup.send("停止播放")
        except KeyError:
            pass
    
    async def play_song(self, interaction: discord.Interaction, url: str):
        if interaction.guild_id not in self.guilds_music.keys():
            voice_client = await interaction.user.voice.channel.connect()
            self.guilds_music[interaction.guild_id] = Music(voice_client)
        
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))
            song = data['url']
            guild_music = self.guilds_music[interaction.guild_id]
            
            if not guild_music.is_playing():
                voice_client = guild_music.get_voice_client()
                voice_client.play(
                    discord.FFmpegPCMAudio(song, **FFMPEG_OPTIONS, executable=FFMPEG_PATH), 
                    after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(interaction), self.bot.loop))
                guild_music.set_playing(True)
            else:
                guild_music.add_song(url, interaction.user)
            return True
        except Exception as e:
            print(e)
            return False

    async def play_next(self, interaction: discord.Interaction):
        try:
            guild_music = self.guilds_music[interaction.guild_id]
            next_song = guild_music.next_song()
        except KeyError:
            return
        
        if next_song is None:
            if guild_music.get_auto_play():
                next_song = 'https://www.youtube.com/watch?v=' + random.choice(self.recommended_songs)
            else:
                guild_music.set_playing(False)
                await guild_music.get_voice_client().disconnect()
                del self.guilds_music[interaction.guild_id]
                return
            
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(next_song, download=False))
            song = data['url']

            player = discord.FFmpegPCMAudio(song, **FFMPEG_OPTIONS, executable=FFMPEG_PATH)
            voice_client = guild_music.get_voice_client()
            voice_client.play(
                player,
                after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(interaction), self.bot.loop)
            )
        except Exception as e:
            print(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(PlaySong(bot), guild=discord.Object(id= os.getenv('GUILD_ID')))