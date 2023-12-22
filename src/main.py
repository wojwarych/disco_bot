import os
import logging

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

from msg_builder import MsgBuilder

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
logger = logging.getLogger(__name__)
bot = Bot(command_prefix="$", intents=discord.Intents.all())


@bot.event
async def on_ready():
    logger.debug("Connected!")


@bot.command()
async def bless(ctx):
    msg_builder = MsgBuilder(message=ctx.message)
    await ctx.send(msg_builder.bless())


if __name__ == "__main__":
    bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
