import pytest
from pytest_mock import MockerFixture

from disco_bot.main import sanitize_guild_names


class FakeGuild:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name


@pytest.mark.parametrize(
    "guild,expected",
    [
        (FakeGuild("Bolzga"), "bolzga"),
        (FakeGuild("some random name"), "some-random-name"),
        (FakeGuild("ALL CAPS MAN"), "all-caps-man"),
        (FakeGuild("Just-a-title"), "just-a-title"),
    ],
)
def test_sanitize_guild_names_returns_lower_and_dashed_guild_names(
    guild: str, expected: str, mocker: MockerFixture
) -> None:
    mock_bot = mocker.MagicMock()
    mock_bot.guilds = [guild]
    assert sanitize_guild_names(mock_bot) == [expected]
