import discord


class MsgBuilder:  # pylint: disable=too-few-public-methods

    def __init__(self, message: discord.Message) -> None:
        self.msg = message

    def bless(self) -> str:
        return f"Szczęść Boże, {self.msg.author.global_name}!"
