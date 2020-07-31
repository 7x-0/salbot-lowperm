"""
Created by vcokltfre - 2020-07-31
"""

from discord.ext import commands
from gtts import gTTS
import discord
from helpers.config import ConfigUtil
import json
import random

config = {
    "permissions": {
        "admin": [],
        "mod": [],
        "user": []
    },
    "enabled": True,
    "listener_channels":[],
    "command_prefixes": ["%", "!", "?"]
}

langs = ["en-uk", "en-us", "en-au"]


class Tts(commands.Cog):
    """Text to speech for voice"""

    def __init__(self, bot):
        self.bot = bot
        self.cfg = ConfigUtil("vctts", config)
        self.vc = None

    def has_perms(self, uid: int, permtype: str) -> bool:
        cfg = self.cfg.read()
        user = cfg["permissions"]["user"]
        mod = cfg["permissions"]["mod"]
        admin = cfg["permissions"]["admin"]
        if permtype == "user":
            return uid in user or uid in mod or uid in admin
        if permtype == "mod":
            return uid in mod or uid in admin
        if permtype == "admin":
            return uid in admin

    @commands.group(name="vcperms")
    @commands.has_any_role("Administrator", "Moderator")
    async def vcperms(self, ctx: commands.Context):
        if ctx.invoked_subcommand == None:
            await ctx.channel.send(f"```json\n{json.dumps(self.cfg.read(), indent=2)}```")

    @vcperms.command(name="forcegrant")
    @commands.has_any_role("Administrator")
    async def vcpforce(self, ctx, uid: int, permtype):
        perms = config["permissions"][permtype]
        if not uid in perms:
            config["permissions"][permtype].append(uid)
            await ctx.channel.send(f"Granted permission node {permtype} for {uid}")
        else:
            await ctx.channel.send(f"This permission node is already granted for this user!")
        self.cfg.write(config)

    @vcperms.command(name="grant")
    async def vcpgrant(self, ctx, uid: int, permtype):
        if not self.has_perms(ctx.author.id, "admin"):
            await ctx.channel.send("You are not permitted to perform this action.")
            return
        config = self.cfg.read()
        perms = config["permissions"][permtype]
        if not uid in perms:
            config["permissions"][permtype].append(uid)
            await ctx.channel.send(f"Granted permission node {permtype} for {uid}")
        else:
            await ctx.channel.send(f"This permission node is already granted for this user!")
        self.cfg.write(config)

    @vcperms.command(name="deny")
    async def vcpdeny(self, ctx, uid: int, permtype):
        if not self.has_perms(ctx.author.id, "admin"):
            await ctx.channel.send("You are not permitted to perform this action.")
            return
        config = self.cfg.read()
        perms = config["permissions"][permtype]
        if uid in perms:
            config["permissions"][permtype].pop(config["permissions"][permtype].index(uid))
            await ctx.channel.send(f"Denied permission node {permtype} for {uid}")
        else:
            await ctx.channel.send(f"This permission node is already denied for this user!")
        self.cfg.write(config)

    @vcperms.command(name="addchannel")
    async def vcpaddchannel(self, ctx, channelid: int):
        if not self.has_perms(ctx.author.id, "admin"):
            await ctx.channel.send("You are not permitted to perform this action.")
            return
        config = self.cfg.read()
        channels = config["listener_channels"]
        if not channelid in channels:
            config["listener_channels"].append(channelid)
            await ctx.channel.send(f"Added listener channel for {channelid}")
        else:
            await ctx.channel.send(f"This channel is already in the listener channels list.")
        self.cfg.write(config)

    @vcperms.command(name="removechannel")
    async def vcprmchannel(self, ctx, channelid: int):
        if not self.has_perms(ctx.author.id, "admin"):
            await ctx.channel.send("You are not permitted to perform this action.")
            return
        config = self.cfg.read()
        channels = config["listener_channels"]
        if channelid in channels:
            config["listener_channels"].pop(config["listener_channels"].index(channelid))
            await ctx.channel.send(f"Removed listener channel for {channelid}")
        else:
            await ctx.channel.send(f"This channel is already in the listener channels list.")
        self.cfg.write(config)

    @vcperms.command(name="enable")
    async def vcpenable(self, ctx):
        config = self.cfg.read()
        config["enabled"] = True
        self.cfg.write(config)
        await ctx.channel.send("Enabled VCTTS")

    @vcperms.command(name="disable")
    async def vcpdisable(self, ctx):
        config = self.cfg.read()
        config["enabled"] = True
        self.cfg.write(config)
        await ctx.channel.send("Disabled VCTTS")

    @commands.command(name="vcjoin")
    async def jvc(self, ctx):
        if not self.has_perms(ctx.author.id, "mod"):
            await ctx.channel.send("You are not permitted to perform this action.")
            return
        channel = ctx.author.voice.channel
        self.vc = await channel.connect()

    @commands.command(name="vcleave")
    async def leave(self, ctx):
        if not self.has_perms(ctx.author.id, "mod"):
            await ctx.channel.send("You are not permitted to perform this action.")
            return
        await ctx.voice_client.disconnect()
        self.vc = None

    @commands.command(name="vcsay")
    async def vcsay(self, ctx, *text):
        if not self.vc:
            return

        if not self.has_perms(ctx.author.id, "mod"):
            await ctx.channel.send("You are not permitted to perform this action.")
            return

        text = " ".join(text)
        obj = gTTS(text=f"{ctx.author.name if not ctx.author.name == 'vcokltfre' else 'v c o'} says {text}", lang=random.choice(langs), slow=False)
        obj.save("data/voice.mp3")
        self.vc.play(discord.FFmpegPCMAudio("data/voice.mp3"))

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.vc or not self.cfg.read()["enabled"]:
            return

        if not self.has_perms(message.author.id, "user"):
            return

        if not message.channel.id in self.cfg.read()["listener_channels"]:
            return

        if any(message.content.startswith(x) for x in self.cfg.read()["command_prefixes"]):
            return

        text = message.content
        customlang = None
        if message.author.id == 297045071457681409 and message.content.startswith("cy"):
            customlang = 'cy'
            text = text.split(" ", 1)[1]

        lang = random.choice(langs) if not customlang else customlang
        obj = gTTS(text=f"{message.author.name if not message.author.name == 'vcokltfre' else 'v c o'} says {text}", lang=lang, slow=False)
        obj.save("data/voice.mp3")
        try:
            self.vc.play(discord.FFmpegPCMAudio("data/voice.mp3"))
        except:
            print("Error: cannot play 2 audio streams simultaneously.")

def setup(bot):
    bot.add_cog(Tts(bot))
