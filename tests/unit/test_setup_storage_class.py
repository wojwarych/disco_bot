# pylint: disable=redefined-outer-name
import pytest

from disco_bot.kremufczan import MockBucketStorage
from disco_bot.main import QUOTES_FILE_KEYNAME, SetupStorage


@pytest.fixture
def bucket_storage() -> MockBucketStorage:
    return MockBucketStorage()


@pytest.fixture
def bucket_storage_with_data() -> MockBucketStorage:
    return MockBucketStorage(data={"random str": []})


def test_setup_storage_is_a_singleton_instance(
    bucket_storage: MockBucketStorage,
) -> None:
    cmd_instance1 = SetupStorage(bucket_storage)
    cmd_instance2 = SetupStorage(bucket_storage)

    assert id(cmd_instance1) == id(cmd_instance2)
    assert not cmd_instance1.command_executed
    assert not cmd_instance2.command_executed


def test_setup_storage_command_executed_true_process_finished(
    bucket_storage: MockBucketStorage,
) -> None:
    stp_strg = SetupStorage(bucket_storage)

    with stp_strg.start_process() as proc:
        proc.run_command("random str", QUOTES_FILE_KEYNAME)

    assert stp_strg.command_executed is True
