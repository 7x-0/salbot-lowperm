"""
Created by vcokltfre - 2020-07-21
"""

import discord
from discord.ext import commands
from helpers.checks import botspam
from helpers.conversions import getRGBfromI, getIfromRGB


class Convert(commands.Cog):
    """Various conversions"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="irgb")
    @botspam
    async def irgb(self, ctx, i: int):
        """Get RGB values from an integer"""
        await ctx.channel.send(str(getRGBfromI(i)))

    @commands.command(name="rgbi")
    @botspam
    async def rgbi(self, ctx, r: int, g: int, b: int):
        """Get an integer from RGB values"""
        await ctx.channel.send(str(getIfromRGB(r,b,g)))


def setup(bot: commands.Bot):
    bot.add_cog(Convert(bot))