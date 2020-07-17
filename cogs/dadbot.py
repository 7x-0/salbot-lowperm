"""
Created by vcokltfre - 2020-07-17
"""

import discord
from discord.ext import commands
from discord.ext.commands import has_any_role
import json
from helpers.config import make_cfg, write_cfg


class Dadbot(commands.Cog):
    """Replies to messages beginning with I'm"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        make_cfg("dadbot", {
            "channel_blacklist":[],
            "person_blacklist":[],
            "enabled":True
        })

    def get_config(self) -> dict:
        with open("./data/dadbot.json") as f:
            return json.load(f)

    def add_blacklist(self, typ: str, uid: int):
        cfg = self.get_config()
        cfg[f"{typ}_blacklist"].append(uid) if not uid in cfg[f"{typ}_blacklist"] else None
        write_cfg("dadbot", cfg)

    def remove_blacklist(self, typ: str, uid: int):
        cfg = self.get_config()
        cfg[f"{typ}_blacklist"].pop(cfg[f"{typ}_blacklist"].index(uid)) if uid in cfg[f"{typ}_blacklist"] else None
        write_cfg("dadbot", cfg)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        cfg = self.get_config()
        if message.author.id in cfg[f"person_blacklist"] or message.channel.id in cfg[f"channel_blacklist"] or not cfg["enabled"]:
            return
        content = message.content.lower()
        if content.startswith("i'm ") or content.startswith('im '):
            await message.channel.send(f"Hi, {content.split(' ',1)[1]}, I'm Dad")

    @commands.group(name="dad")
    @has_any_role("Moderator", "Administrator")
    async def dad(self, ctx: commands.Context):
        """Dad bot moderation commands"""
        if ctx.invoked_subcommand == None:
            await ctx.channel.send("Invalid subcommand. Usage: `%dad <channel | person | list | enable | disable> [<allow | block>] [<channel_id | user_id>]`")

    @dad.command(name="channel")
    async def dadchannel(self, ctx: commands.Context, subcommand: str, channel_id: int):
        """Add or remove a channel from the dad bot blacklist"""
        if subcommand == "allow":
            self.remove_blacklist("channel", channel_id)
        elif subcommand == "block":
            self.add_blacklist("channel", channel_id)

    @dad.command(name="person")
    async def dadperson(self, ctx: commands.Context, subcommand: str, user_id: int):
        """Add or remove a person from the dad bot blacklist"""
        if subcommand == "allow":
            self.remove_blacklist("person", user_id)
        elif subcommand == "block":
            self.add_blacklist("person", user_id)

    @dad.command(name="list")
    async def dadlist(self, ctx: commands.Context):
        """List channel and user IDs in the blacklist"""
        cfg = self.get_config()
        channels = "\n".join([str(i) for i in cfg["channel_blacklist"]])
        people = "\n".join([str(i) for i in cfg["person_blacklist"]])

        embed = discord.Embed(title="Dad bot blacklists")
        embed.add_field(name="Channels", value=channels) if len(cfg["channel_blacklist"]) > 0 else None
        embed.add_field(name="People", value=people) if len(cfg["person_blacklist"]) > 0 else None

        await ctx.channel.send(embed=embed)

    @dad.command(name="enable")
    async def dadenable(self, ctx: commands.Context):
        """Enable dad bot responses persistently"""
        cfg = self.get_config()
        cfg["enabled"] = True
        write_cfg("dadbot", cfg)
        await ctx.channel.send("Enabled dad bot responses.")

    @dad.command(name="disable")
    async def daddisable(self, ctx: commands.Context):
        """Disable dad bot responses persistently"""
        cfg = self.get_config()
        cfg["enabled"] = False
        write_cfg("dadbot", cfg)
        await ctx.channel.send("Disabled dad bot responses.")


def setup(bot: commands.Bot):
    bot.add_cog(Dadbot(bot))