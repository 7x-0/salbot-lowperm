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
    @botspam()
    async def irgb(self, ctx, i: int):
        """Get RGB values from an integer"""
        if i > 16777215 or i < 0:
            await ctx.channel.send("The number you entered was invalid. It must be in the range 0 to 16777215", delete_after=15)
            return
        embed=discord.Embed(title=f"{getRGBfromI(i)}", colour=i)
        await ctx.channel.send(embed=embed)

    @commands.command(name="rgbi")
    @botspam()
    async def rgbi(self, ctx, r: int, g: int, b: int):
        """Get an integer from RGB values"""
        if r > 255 or g > 255 or b > 255 or r < 0 or g < 0 or b < 0:
            await ctx.channel.send("One or more of the values you entered was invalid. RGB values must range from 0 to 255", delete_after=15)
            return
        embed=discord.Embed(title=f"{getIfromRGB((r,g,b))}", colour=getIfromRGB((r,g,b)))
        await ctx.channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Convert(bot))