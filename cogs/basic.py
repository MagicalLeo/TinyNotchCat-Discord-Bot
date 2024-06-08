import discord
from discord import app_commands
from discord.ext import commands

class Basic(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ping command
    @app_commands.command(name = "ping", description = "Ping the bot")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message("Ping: " + str(latency) + "ms")

async def setup(bot: commands.Bot):
    await bot.add_cog(Basic(bot))