import random
from typing import Any

import discord


class MsgBuilder:  # pylint: disable=too-few-public-methods
    def bless(self, message: discord.Message) -> str:
        return f"Szczęść Boże, {message.author.global_name}!"

    def kremufka(self, quote_body: dict[str, Any]) -> str:
        return random.choice(quote_body["Body"].readlines()).decode("utf-8").strip()
