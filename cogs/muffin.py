"""
Created by vcokltfre - 2020-07-19
"""

import discord
from discord.ext import commands
from helpers.checks import botspam
import random


class Muffin(commands.Cog):
    """Do you want a muffin?"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="muffin")
    @botspam()
    async def muffin(self, ctx: commands.Context):
        """Gives the user a muffin... maybe"""
        if random.randint(0,3) != 2:
            with open("static_data/muffin.jpg", 'rb') as f:
                await ctx.channel.send(file=discord.File(f))
        else:
            await ctx.channel.send("No muffin for you!")



def setup(bot: commands.Bot):
    bot.add_cog(Muffin(bot))