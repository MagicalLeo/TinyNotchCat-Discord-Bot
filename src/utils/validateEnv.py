import os

def validate_env():
    if os.getenv('DISCORD_TOKEN') is None:
        return False
    if os.getenv('SPOTIFY_SECRET') is None:
        return False
    return True