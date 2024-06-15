import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from typing import Optional
from .components.complaints import Complaint

class Complain(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.complaint = Complaint()
    
    # complain command
    @app_commands.command(name = "complain", description = "抱怨箱online")
    @app_commands.describe(method = "選擇餐點", text = "說點啥吧")
    @app_commands.choices(
        method = [
            Choice(name = "提交", value = "add"),
            Choice(name = "抽獎", value = "get"),
            Choice(name = "清空", value = "clear"),
        ]
    )
    async def complain(self, interaction: discord.Interaction, method: Choice[str], text: Optional[str] = None):
        if method.value == "add":
            self.complaint.add_complaint(text)
            await interaction.response.send_message("抱怨已收到")
        elif method.value == "get":
            complaint = self.complaint.get_complaint()
            if complaint:
                await interaction.response.send_message(complaint)
            else:
                await interaction.response.send_message("抱怨箱是空的")
        elif method.value == "clear":
            self.complaint.clear_complaints()
            await interaction.response.send_message("抱怨箱已清空")

async def setup(bot: commands.Bot):
    await bot.add_cog(Complain(bot), guild=discord.Object(id= os.getenv('GUILD_ID')))
        