from __future__ import annotations

import asyncio
import logging
import logging.handlers
import os
import sys
from collections.abc import Iterator
from contextlib import contextmanager

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

from .kremufczan import BucketStorage
from .msg_builder import MsgBuilder
from .scheduler import PapajScheduler

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

QUOTES_FILE_KEYNAME = "mondrosci.txt"


class Singleton(type):
    _instances: dict[type, str] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SetupStorage(metaclass=Singleton):
    def __init__(self, storage_client: BucketStorage) -> None:
        self.storage_client = storage_client
        self.command_executed = False

    def run_command(self, bucket_name: str, key: str) -> dict[str, str]:
        logger.info(bucket_name)
        self.storage_client.create_bucket(bucket_name=bucket_name)
        self.storage_client.init_object(bucket_name, key)
        return {"Message": "Completed"}

    def finished(self) -> None:
        self.command_executed = self.command_executed or True

    @contextmanager
    def start_process(self) -> Iterator[SetupStorage]:
        try:
            yield self
        finally:
            self.finished()


bot = Bot(command_prefix="$", intents=discord.Intents.all())


@bot.event
async def on_ready():
    logger.info("Connected!")
    logger.info("Performing Storage Check and creation...")
    storage_client = BucketStorage()
    storage_setup = SetupStorage(storage_client=storage_client)
    guilds = sanitize_guild_names(bot)
    with storage_setup.start_process() as st_proc:
        for guild in guilds:
            ret = st_proc.run_command(guild, QUOTES_FILE_KEYNAME)
            logger.info(ret)
    logger.info("Successfully finished!")


def sanitize_guild_names(bot_instance: Bot) -> list[str]:
    return [guild.name.replace(" ", "-").lower() for guild in bot_instance.guilds]


@bot.command(name="bless")
async def bless(ctx):
    msg_builder = MsgBuilder()
    await ctx.send(msg_builder.bless(ctx.message))


@bot.group(name="kremufka")
async def kremufka(ctx): ...  # pylint: disable=unused-argument


@kremufka.command(name="dej")
async def dej(ctx):
    storage = BucketStorage()
    guild_name = ctx.guild.name.replace(" ", "-").lower()
    ret = storage.get_object(guild_name, QUOTES_FILE_KEYNAME)
    msg_builder = MsgBuilder()
    await ctx.send(msg_builder.kremufka(ret))


@kremufka.command(name="dodej")
async def dodej(ctx, *, args):
    storage = BucketStorage()
    guild_name = ctx.guild.name.replace(" ", "-").lower()
    ret = storage.add_quote_to_object(guild_name, QUOTES_FILE_KEYNAME, args)
    logger.info(ret)
    await ctx.send("Bóg zapłać!")


async def main(bot):  # pylint: disable=redefined-outer-name
    async with bot:
        await bot.add_cog(PapajScheduler(bot, BARKA_CHANNEL_ID))
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main(bot))
