import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from src.utils.validateEnv import validate_env
from cogs.components.commands import Commands

if not validate_env():
    print('Environment variables not set correctly.')
    exit()
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SPOTITY_SECRET = os.getenv('SPOTIFY_SECRET')
GUILD_ID = os.getenv('GUILD_ID')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
# 當機器人完成啟動
async def on_ready(): 
    slash = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"目前登入身份 --> {bot.user}")
    print(f"載入 {len(slash)} 個斜線指令")
    write_helps()
    print('載入 Help command')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('從北京跑到巴黎'))


@bot.command()
async def load(ctx: commands.Context, extension: str):
    try:
        await bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} loaded')
    except:
        await ctx.send(f'{extension} not found')

@bot.command()
async def unload(ctx: commands.Context, extension: str):
    try:
        await bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} unloaded')
    except:
        await ctx.send(f'{extension} not found')

@bot.command()
async def reload(ctx: commands.Context, extension: str):
    try:
        await bot.reload_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} reloaded')
    except:
        await ctx.send(f'{extension} not found')

def write_helps():
    commands = Commands()
    all_commands = {}
    for slash_command in bot.tree.walk_commands(guild=discord.Object(id=GUILD_ID)):
        all_commands[slash_command.name] = slash_command.description if slash_command.description else slash_command.name
    commands.save_commands(all_commands)

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