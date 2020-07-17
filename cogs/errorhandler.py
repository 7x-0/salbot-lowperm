"""
Created by Epic - 2020-07-17
"""

import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    """A description of what this cog does"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(str(error))
        else:
            await ctx.send("Oops, something broke.")


def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
