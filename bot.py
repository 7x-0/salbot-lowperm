"""
Created by vcokltfre - 2020-07-15
"""

import discord
from discord.ext import commands

import logging
from salbotlp_secrets.config import TOKEN

logger = logging.getLogger("salbot_lp")


class Bot(commands.Bot):
    """A subclassed version of commands.Bot"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_cog(self, cog: commands.Cog) -> None:
        """Adds a cog to the bot and logs it."""
        super().add_cog(cog)
        logger.info(f"Cog loaded: {cog.qualified_name}")

    def load_extensions(self, cogs: list):
        """Loads a list of cogs"""
        for cog in cogs:
            try:
                super().load_extension()
                logger.info(f"Loaded cog {cog} successfully.")
            except:
                logger.error(f"Failed to load cog {cog}.")

    async def on_error(self, event: str, *args, **kwargs) -> None:
        """Log errors raised in event listeners rather than printing them to stderr."""

        logger.exception(f"Unhandled exception in {event}.", exc_info=True)


if __name__ == "__main__":
    bot = Bot(
        command_prefix=commands.when_mentioned_or("%"),
        max_messages=10000,
        allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False)
        )

    cogs = []

    bot.load_extensions(cogs)
    bot.run(TOKEN)