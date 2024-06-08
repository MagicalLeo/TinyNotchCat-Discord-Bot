import discord
from discord import app_commands
from discord.ext import commands

class Complain(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "complain", description = "抱怨箱online")
    @app_commands.describe(a = "輸入數字", b = "輸入數字")
    async def complain(self, interaction: discord.Interaction, a: int, b: int):
        await interaction.response.send_message(f"結果: {a+b}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Complain(bot))
        