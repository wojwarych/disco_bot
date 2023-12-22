import abc
import logging

import discord
from discord.ext.commands import Bot

logger = logging.getLogger(__name__)


class MsgBuilder:

    def __init__(self, message: discord.Message) -> None:
        self.msg = message

    def bless(self) -> str:
        return f"Szczęść Boże, {self.msg.author.global_name}!"
