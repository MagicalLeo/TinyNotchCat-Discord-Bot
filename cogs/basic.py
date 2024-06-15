import os
import discord
from discord import app_commands
from discord.ext import commands
from .components.commands import Commands

class Basic(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.commands = Commands()

    # help command
    @app_commands.command(name="help", description="需要幫助?")
    async def help(self, interaction: discord.Interaction):
        em = discord.Embed(
            title="Help",
            description="所有指令",
            color=discord.Color.blurple()
        )
        em.set_thumbnail(
            url=self.bot.user.avatar.url
        )
        for command_name, description in self.commands.get_command_dict().items():
            em.add_field(
                name= "/" + command_name,
                value= description,
                inline=False
            ) 
        await interaction.response.send_message(embed=em)

    # ping command
    @app_commands.command(name = "ping", description = "顯示延遲")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message("Ping: " + str(latency) + "ms")

async def setup(bot: commands.Bot):
    await bot.add_cog(Basic(bot), guild=discord.Object(id= os.getenv('GUILD_ID')))