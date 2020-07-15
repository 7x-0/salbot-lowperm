"""
Created by vcokltfre - 2020-07-15
"""

from discord.ext import commands
from salbotlp_secrets.config import MOD_ROLES, BOT_SPAM_CHANNELS, BOT_SPAM_ONLY

def botspam():
    async def check(ctx: commands.Context):
        if not BOT_SPAM_ONLY:
            return True

        if any([i.name in MOD_ROLES for i in ctx.author.roles]) or ctx.channel.id in BOT_SPAM_CHANNELS:
            return True

        raise commands.errors.MissingPermissions(["BotspamOverride"])

    return commands.check(check)