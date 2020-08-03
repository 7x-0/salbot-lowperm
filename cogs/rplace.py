"""
Created by vcokltfre - 2020-07-31
"""

import discord
from discord.ext import commands
from pathlib import Path
from PIL import Image
from helpers.config import ConfigUtil
from helpers.checks import botspam


class RSPlace(commands.Cog):
    """/r/place, but smaller and on Salbot"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if not Path("data/rplace.png").exists():
            img = Image.new("RGB", (256, 256), color = (0, 0, 0))
            img.save("data/rplace.png")
        self.im = Image.open("data/rplace.png")
        self.cfg = ConfigUtil("rplace", {"editcount": 0, "edits": []})

    def isvalid(self, value: int):
        if value < 256 and value > -1:
            return True
        return False

    def call_update(self, user: int, name: str, pval: tuple):
        data = self.cfg.read()
        data["editcount"] += 1
        data["edits"].append({"name": name, "id": user, "pixelValuePair": pval})
        self.cfg.write(data)
        if data["editcount"] % 5 == 0:
            self.im.save("data/rplace.png")

    @commands.command(name="rplace", aliases=["rp"])
    @botspam()
    async def rplace(self, ctx: commands.Context, pixelx: int, pixely: int, red: int, green: int, blue: int):
        print("rp")
        values = [not self.isvalid(item) for item in [pixelx, pixely, red, green, blue]]
        if any(values):
            await ctx.channel.send("One of your values was invalid. They must each be an integer from 0-255\nUsage: `%rplace <x> <y> <r> <g> <b>` where x=0 y=0 is the top left corner")
        self.im.putpixel((pixelx, pixely), (red, green, blue))
        self.call_update(ctx.author.name, ctx.author.id, (pixelx, pixely, red, green, blue))

    @commands.command(name="rpshow")
    @botspam()
    async def rpshow(self, ctx: commands.Context):
        self.im.save("data/rplace.png")
        with Path("data/rplace.png").open('rb') as f:
            await ctx.channel.send(file=discord.File(f, filename="rplace.png"))

    @commands.command(name="export")
    @commands.has_any_role("Administrator")
    async def rpexport(self, ctx: commands.Context):
        await ctx.channel.send(file=discord.File(fp="data/rplace.json"))


def setup(bot: commands.Bot):
    bot.add_cog(RSPlace(bot))