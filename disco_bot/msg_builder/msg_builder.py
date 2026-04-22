import random
from typing import Any

import discord


class EmptyQuotesFile(Exception): ...


class MsgBuilder:  # pylint: disable=too-few-public-methods
    def bless(self, message: discord.Message) -> str:
        return f"Szczęść Boże, {message.author.global_name}!"

    def kremufka(self, quote_body: dict[str, Any]) -> str:
        try:
            text = quote_body["Body"].read_text(encoding="utf-8").split("\n")
            return random.choice(text)
        except IndexError as e:
            raise EmptyQuotesFile("Resource for quotes is empty!") from e
