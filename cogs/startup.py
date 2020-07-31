"""
Created by vcokltfre - 2020-07-31
"""

import discord
from discord.ext import commands
import time
from helpers.config import ConfigUtil


class Startup(commands.Cog):
    """Runs events on bot startup"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        cfg = ConfigUtil("rslock", {"lock": 0})
        data = cfg.read()
        print(data, time.time())
        if data["lock"] > time.time():
            chann = self.bot.get_channel(data["channel"])
            await chann.send("Restart Successful!", delete_after=15)


def setup(bot: commands.Bot):
    bot.add_cog(Startup(bot))