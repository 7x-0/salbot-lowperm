"""
Created by vcokltfre - 2020-07-15
"""

import discord
from discord.ext import commands
from googletrans import Translator
from helpers.checks import botspam


class Translate(commands.Cog):
    """A cog to translate messages between languages"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.trans = Translator()

    @commands.group(name="translate", aliases=["tl"])
    @botspam()
    async def translate(self, ctx: commands.Context):
        """A group of commands to translate text"""
        if ctx.invoked_subcommand == None:
            await ctx.channel.send("Invalid subcommand. Usage: `%translate [auto | from | to | 2way] [from] [to] *text`")

    @translate.command(name="auto")
    async def tlauto(self, ctx: commands.Context, *text):
        """Automatically translate the given text into English"""
        text = " ".join(text)

        translated = self.trans.translate(text)
        src = translated.src
        txt = translated.text

        embed = discord.Embed(title="Translate", description=f"Translating from {src} to English")
        embed.add_field(name="Source Text", value=text)
        embed.add_field(name="Result Text", value=txt)

        await ctx.channel.send(embed=embed)

    @translate.command(name="from")
    async def tlfrom(self, ctx: commands.Context, src: str, *text):
        """Translate text from a given language into English"""
        text = " ".join(text)

        translated = self.trans.translate(text, src=src)
        txt = translated.text

        embed = discord.Embed(title="Translate", description=f"Translating from {src} to English")
        embed.add_field(name="Source Text", value=text)
        embed.add_field(name="Result Text", value=txt)

        await ctx.channel.send(embed=embed)

    @translate.command(name="to")
    async def tlto(self, ctx: commands.Context, dest: str, *text):
        """Translate text from English to a given language"""
        text = " ".join(text)

        translated = self.trans.translate(text, dest=dest)
        txt = translated.text

        embed = discord.Embed(title="Translate", description=f"Translating from English to {dest}")
        embed.add_field(name="Source Text", value=text)
        embed.add_field(name="Result Text", value=txt)

        await ctx.channel.send(embed=embed)

    @translate.command(name="2way")
    async def tl2way(self, ctx: commands.Context, src: str, dest: str, *text):
        """Translate text between two given languages"""
        text = " ".join(text)

        translated = self.trans.translate(text, src=src, dest=dest)
        txt = translated.text

        embed = discord.Embed(title="Translate", description=f"Translating from {src} to {dest}")
        embed.add_field(name="Source Text", value=text)
        embed.add_field(name="Result Text", value=txt)

        await ctx.channel.send(embed=embed)

    @translate.command(name="binascii")
    async def tlbinascii(self, ctx: commands.Context, *text):
        """Translate text from binary (eg. 10110000 10100011) to ASCII"""
        text = " ".join(text)

        txt = "".join(chr(int(f"0b{x}",2)) for x in text.split(' '))

        embed = discord.Embed(title="Translate", description=f"Translating from binary to ASCII")
        embed.add_field(name="Result Text", value=txt)

        await ctx.channel.send(embed=embed)

    @translate.command(name="asciibin")
    async def tlasciibin(self, ctx: commands.Context, *text):
        """Translate text from ASCII to binary"""
        text = " ".join(text)

        txt =  " ".join(bin(ord(x)).replace('0b','') for x in text)

        embed = discord.Embed(title="Translate", description=f"Translating from ASCII to binary")
        embed.add_field(name="Result Text", value=txt)

        await ctx.channel.send(embed=embed)

    @translate.error
    async def tlerr(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.delete()
            await ctx.channel.send("This command can only be used in bot spam channels.", delete_after=10)


def setup(bot: commands.Bot):
    bot.add_cog(Translate(bot))