"""
Created by Epic - 2020-07-17
"""

import discord
from discord.ext import commands
from helpers.checks import botspam, MOD_ROLES
from salbotlp_secrets.config import BADGES
from helpers.config import ConfigUtil


class Profile(commands.Cog):
    """Adds a profile command"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.config = ConfigUtil("badges", default={})

    @commands.command()
    @botspam()
    async def profile(self, ctx: commands.Context, user: discord.User = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed()
        embed.set_author(name=user, icon_url="https://cdn.discordapp.com/emojis/547141731850780672.png")
        embed.colour = 0x00FFFF

        badges = self.config.read().get(str(user.id), [])
        description = "Badges:\n"
        for badge in badges:
            description += f"{BADGES[badge]} {badge}\n"
        embed.description = description

        await ctx.send(embed=embed)

    @commands.group()
    @commands.has_any_role(*MOD_ROLES)
    async def badge(self, ctx):
        pass

    @badge.command()
    async def give(self, ctx, user: discord.User, badge):
        config = self.config.read()
        badge = badge.lower()
        user_badges = config.get(user.id, [])
        if badge in user_badges:
            return await ctx.send("This user already has this badge!")
        user_badges.append(badge)
        config[str(user.id)] = user_badges
        self.config.write(config)
        await ctx.send("Done")


def setup(bot: commands.Bot):
    bot.add_cog(Profile(bot))
