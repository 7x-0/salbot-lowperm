"""
Created by vcokltfre - 2020-07-31
"""

import discord
from discord.ext import commands
from helpers.checks import botspam
from helpers.conversions import getRGBfromI, getIfromRGB


class Convert(commands.Cog):
    """General commands for sblp"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="say")
    @commands.has_any_role("Administrator")
    async def irgb(self, ctx, *text):
        """Says something"""
        text = " ".join(text)
        await ctx.channel.send(text)


def setup(bot: commands.Bot):
    bot.add_cog(Convert(bot))