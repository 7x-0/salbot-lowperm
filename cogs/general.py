"""
Created by vcokltfre - 2020-07-31
"""

import discord
from discord.ext import commands
import requests
import json
from salbotlp_secrets.config import HOOK


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

    @commands.command(name="shut")
    @commands.has_any_role("Administrator", "Moderator", "Private Chat Access")
    async def shut(self, ctx: commands.Context):
        await ctx.channel.send("https://shutplea.se")
        await ctx.message.delete()

    @commands.command(name="dude")
    @commands.has_any_role("Administrator", "Moderator", "Private Chat Access")
    async def dude(self, ctx: commands.Context):
        await ctx.channel.send("https://shutupdu.de")
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print("com")
        data = {
            "username":str(ctx.author),
            "avatar_url":str(ctx.author.avatar_url),
            "content":f"Executed command: {ctx.message.content}"
        }
        #requests.post(HOOK, data=json.dumps(data), headers={"Content-Type": "application/json"})


def setup(bot: commands.Bot):
    bot.add_cog(Convert(bot))