from unittest.mock import Mock

from hypothesis import given
from hypothesis import strategies as st

from disco_bot.msg_builder import MsgBuilder


@given(st.text())
def test_msg_builder_bless(rand_str: str) -> None:
    msg_mock = Mock()
    msg_mock.author.global_name = rand_str
    msg_builder = MsgBuilder()

    assert (
        msg_builder.bless(message=msg_mock)
        == f"Szczęść Boże, {msg_mock.author.global_name}!"
    )
