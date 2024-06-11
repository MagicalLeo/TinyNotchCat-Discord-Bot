import os

def validate_env():
    if os.getenv('DISCORD_TOKEN') is None:
        return False
    if os.getenv('FFMPEG_PATH') is None:
        return False
    if os.getenv('SPOTIFY_CLIENT_ID') is None:
        return False
    if os.getenv('SPOTIFY_CLIENT_SECRET') is None:
        return False
    return True