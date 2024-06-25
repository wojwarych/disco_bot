import asyncio
import logging
import logging.handlers
import os
import sys

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

from msg_builder import MsgBuilder
from scheduler import PapajScheduler

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
BARKA_CHANNEL_ID = int(os.getenv("BARKA_CHANNEL_ID", ""))


logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename="discord.log",
    encoding="utf-8",
    maxBytes=32 * 1024 * 1024,  # 32MiB
    backupCount=5,
)
stream_handler = logging.StreamHandler(sys.stdout)
stream_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
stream_handler.setFormatter(stream_format)
logger.addHandler(handler)
logger.addHandler(stream_handler)

bot = Bot(command_prefix="$", intents=discord.Intents.all())


@bot.event
async def on_ready():
    logger.info("Connected!")


@bot.command(name="bless")
async def bless(ctx):
    msg_builder = MsgBuilder(message=ctx.message)
    await ctx.send(msg_builder.bless())


async def main(bot):
    async with bot:
        await bot.add_cog(PapajScheduler(bot, BARKA_CHANNEL_ID))
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main(bot))
