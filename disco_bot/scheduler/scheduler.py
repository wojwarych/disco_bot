import asyncio
import datetime
import logging
import logging.handlers
import os
import sys
from zoneinfo import ZoneInfo

from discord.ext import commands, tasks
from discord.ext.commands import Bot
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(sys.stdout)
stream_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
stream_handler.setFormatter(stream_format)
logger.addHandler(stream_handler)

load_dotenv()
BARKA_HOUR = int(os.getenv("BARKA_HOUR", "21"))
BARKA_MINUTE = int(os.getenv("BARKA_MINUTE", "37"))

time = datetime.time(
    hour=BARKA_HOUR, minute=BARKA_MINUTE, tzinfo=ZoneInfo("Europe/Warsaw")
)


class PapajScheduler(commands.Cog):
    def __init__(self, bot: Bot, channel_id: int) -> None:
        self.bot = bot
        self.channel_id = channel_id
        self.papaj_task.start()

    async def cog_unload(self):
        self.papaj_task.cancel()

    @tasks.loop(time=time)
    async def papaj_task(self):
        message_channel = self.bot.get_channel(self.channel_id)
        with open("./disco_bot/papaj.txt", "r", encoding="utf-8") as f:
            for line in f:
                await message_channel.send(line)
                await asyncio.sleep(3)
