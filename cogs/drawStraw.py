import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from .utils.loadData import load_json

class DrawStraw(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        reply = load_json("docs/bot_reply.json")
        self.jokes = reply["jokes"]
        self.foods = reply["foods"]
        self.activities = reply["activities"]
    
    # joke command
    @app_commands.command(name = "joke", description = "講個笑話")
    async def joke(self, interaction: discord.Interaction):
        joke = random.choice(self.jokes)
        await interaction.response.send_message(joke)

    # eat command
    @app_commands.command(name = "eat", description = "今晚想來一點")
    async def eat(self, interaction: discord.Interaction):
        food = random.choice(self.foods)
        await interaction.response.send_message(f"今晚想來一點？{food}")
    
    # do command
    @app_commands.command(name = "do", description = "要幹嘛")
    async def do(self, interaction: discord.Interaction):
        activity = random.choice(self.activities)
        await interaction.response.send_message(f"要幹嘛？{activity}")

    # yesorno command
    @app_commands.command(name = "yesorno", description = "好難決定...")
    async def yesorno(self, interaction: discord.Interaction):
        responses = ["是", "否", "可能", "不確定", "絕對"]
        await interaction.response.send_message(random.choice(responses))

async def setup(bot: commands.Bot):
    await bot.add_cog(DrawStraw(bot), guild=discord.Object(id= os.getenv('GUILD_ID')))