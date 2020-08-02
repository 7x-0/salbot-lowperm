"""
Created by vcokltfre - 2020-08-02
"""

import discord
from discord.ext import commands
from helpers.qrcodes import get_text
import requests


class QRCodes(commands.Cog):
    """Automatically decode QR codes in images in messages"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if len(message.attachments) == 0:
            return
        attach = message.attachments[0]
        filename = attach.filename
        if any([filename.endswith(x) for x in [".png", ".jpg"]]):
            data = requests.get(attach.url)
            with open("data/temp.png", 'wb') as f:
                f.write(data.content)
            texts = get_text("data/temp.png")
            if len(texts) > 0:
                out = ""
                for text in texts:
                    out += f"{text[0]}: {text[1]}\n\n\n"
                with open("data/qrdata.txt", 'w') as f:
                    f.write(out)
                await message.channel.send(file=discord.File(fp="data/qrdata.txt", filename="decoded_qr_data.txt"))


def setup(bot: commands.Bot):
    bot.add_cog(QRCodes(bot))