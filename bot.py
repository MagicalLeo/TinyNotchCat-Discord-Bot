import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from src.components.complaints import load_complaints
from src.utils.validateEnv import validate_env

if not validate_env():
    print('Environment variables not set correctly.')
    exit()
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SPOTITY_SECRET = os.getenv('SPOTIFY_SECRET')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
# 當機器人完成啟動
async def on_ready():
    slash = await bot.tree.sync()
    print(f"目前登入身份 --> {bot.user}")
    print(f"載入 {len(slash)} 個斜線指令")

    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('從北京跑到巴黎'))
    load_complaints()
    print("抱怨列表已加載。")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())