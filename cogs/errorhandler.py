"""
Created by Epic - 2020-07-17
"""

import discord
from discord.ext import commands
import asyncio


class ErrorHandler(commands.Cog):
    """A description of what this cog does"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(str(error), delete_after=15)
            await asyncio.sleep(5)
            await ctx.message.delete()
        else:
            await ctx.send("Oh no! Something went wrong, please us `%help` for help.", delete_after=30)


def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
