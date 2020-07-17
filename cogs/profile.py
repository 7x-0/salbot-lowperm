"""
Created by Epic - 2020-07-17
"""

import discord
from discord.ext import commands
from helpers.checks import botspam, MOD_ROLES
from salbotlp_secrets.config import BADGES
from pathlib import Path
import json


class Profile(commands.Cog):
    """Adds a profile command"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.badge_path = Path() / "salbotlp_secrets" / "badges.json"
        if self.badge_path.exists():
            with self.badge_path.open() as badge_file:
                self.badge_users = json.load(badge_file)
        else:
            self.badge_users = {}

    @commands.command()
    @botspam()
    async def profile(self, ctx: commands.Context, user: discord.User = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed()
        embed.set_author(name=user, icon_url="https://cdn.discordapp.com/emojis/547141731850780672.png")
        embed.colour = 0x00FFFF

        badges = self.badge_users.get(str(user.id), [])
        description = ""
        for badge in badges:
            description += BADGES[badge] + " "
        embed.description = description

        await ctx.send(embed=embed)

    @commands.group()
    @commands.has_any_role(*MOD_ROLES)
    async def badge(self, ctx):
        pass

    @badge.command()
    async def give(self, ctx, user: discord.User, badge):
        badge = badge.lower()
        user_badges = self.badge_users.get(user.id, [])
        if badge in user_badges:
            return await ctx.send("This user already has this badge!")
        user_badges.append(badge)
        self.badge_users[str(user.id)] = user_badges  # Json is stupid, although full database would be overkill for this

        with self.badge_path.open("w") as badge_file:
            json.dump(self.badge_users, badge_file)
        await ctx.send("Done")


def setup(bot: commands.Bot):
    bot.add_cog(Profile(bot))
