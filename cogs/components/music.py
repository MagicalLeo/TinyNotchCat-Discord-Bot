from discord import VoiceClient
from typing import List


class Song:
    def __init__(self, url, user):
        self.url = url
        self.user = user
    
    def __str__(self):
        return self.url

class Music:
    def __init__(self, voice_client: VoiceClient):
        self.voice_client = voice_client
        self.song_queue: List[Song] = []
        self.auto_play = False
        self.playing = False
    
    def add_song(self, url, user):
        self.song_queue.append(Song(url, user))
    
    def next_song(self):
        if self.song_queue:
            return self.song_queue.pop(0).url
        return None
    
    def set_auto_play(self, auto_play):
        self.auto_play = auto_play
    
    def get_now_playing(self):
        if self.song_queue:
            return self.song_queue[0].url, self.song_queue[0].user
        return None, None
    
    def get_voice_client(self):
        return self.voice_client
    
    def get_auto_play(self):
        return self.auto_play
    
    def set_playing(self, playing):
        self.playing = playing

    def is_playing(self):
        return self.playing
