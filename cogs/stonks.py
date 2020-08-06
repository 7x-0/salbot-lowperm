"""
Created by vcokltfre - 2020-08-06
"""

import discord
from discord.ext import commands
from helpers.checks import botspam
from yahoo_fin import stock_info as si


class Stonks(commands.Cog):
    """Get stonks info"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="stonks")
    @botspam()
    async def stonks(self, ctx: commands.Context, stonk: str):
        p = round(si.get_live_price(stonk), 3)
        await ctx.channel.send(f"Stonks for {stonk.upper()}: {p}")



def setup(bot: commands.Bot):
    bot.add_cog(Stonks(bot))