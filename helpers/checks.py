"""
Created by vcokltfre - 2020-07-15
"""

from discord.ext import commands
from salbotlp_secrets.config import MOD_ROLES, BOT_SPAM_CHANNELS, BOT_SPAM_ONLY, USER_BYPASS

def botspam():
    async def check(ctx: commands.Context):
        if not BOT_SPAM_ONLY:
            return True

        if any([i.name in MOD_ROLES for i in ctx.author.roles]) or ctx.channel.id in BOT_SPAM_CHANNELS or ctx.author.id in USER_BYPASS:
            return True

        raise Exception("This command must be ran in a botspam channel or by an overriden user.")

    return commands.check(check)