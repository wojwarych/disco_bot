from unittest.mock import Mock

from hypothesis import given
from hypothesis import strategies as st

from src.msg_builder import MsgBuilder


@given(st.text())
def test_msg_builder_bless(rand_str: str) -> None:
    msg_mock = Mock()
    msg_mock.author.global_name = rand_str
    msg_builder = MsgBuilder(message=msg_mock)

    assert msg_builder.bless() == f"Szczęść Boże, {msg_mock.author.global_name}!"
