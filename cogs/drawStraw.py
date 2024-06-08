import json
import random
import discord
from discord import app_commands
from discord.ext import commands

class DrawStraw(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        reply = self.load_reply("docs/botReply.json")
        self.jokes = reply["jokes"]
        self.foods = reply["foods"]
        self.activities = reply["activities"]

    # Load reply data from json file
    def load_reply(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            reply_data = json.load(f)
        return reply_data
    
    # joke command
    @app_commands.command(name = "joke", description = "講個笑話")
    async def joke(self, interaction: discord.Interaction):
        joke = random.choice(self.jokes)
        await interaction.response.send_message(joke)

    # eat command
    @app_commands.command(name = "eat", description = "晚上吃甚麼")
    async def eat(self, interaction: discord.Interaction):
        food = random.choice(self.foods)
        await interaction.response.send_message(f"晚上吃甚麼？{food}")
    
    # do command
    @app_commands.command(name = "do", description = "要幹嘛")
    async def do(self, interaction: discord.Interaction):
        activity = random.choice(self.activities)
        await interaction.response.send_message(f"要幹嘛？{activity}")

    # yesorno command
    @app_commands.command(name = "yesorno", description = "yesorno")
    async def yesorno(self, interaction: discord.Interaction):
        responses = ["是", "否", "可能", "不確定", "絕對"]
        await interaction.response.send_message(random.choice(responses))

    @app_commands.command(name = "complain", description = "抱怨箱online")
    @app_commands.describe(a = "輸入數字", b = "輸入數字")
    async def complain(self, interaction: discord.Interaction, a: int, b: int):
        await interaction.response.send_message(f"結果: {a+b}")

async def setup(bot: commands.Bot):
    await bot.add_cog(DrawStraw(bot))