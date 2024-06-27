# pylint: disable=redefined-outer-name,unused-argument
import pytest
from pytest_mock import MockerFixture

from disco_bot.kremufczan import BucketStorage
from disco_bot.kremufczan.s3_connection import (
    BucketAlreadyExistsError,
    BucketNotFoundError,
    ObjectNotFoundError,
)


def test_get_object_returns_data(
    bucket: None, s3_object: None, bucket_name: str, object_name: str
) -> None:
    storage = BucketStorage()

    assert storage.get_object(bucket_name, object_name)


def test_get_object_raises_error_on_no_object(
    bucket, bucket_name: str, object_name: str
) -> None:
    storage = BucketStorage()

    with pytest.raises(ObjectNotFoundError):
        storage.get_object(bucket_name, object_name)


def test_get_object_raises_error_on_no_bucket(
    bucket_name: str, object_name: str
) -> None:
    storage = BucketStorage()

    with pytest.raises(BucketNotFoundError):
        storage.get_object(bucket_name, object_name)


def test_init_creates_empty_object(
    s3_client, bucket, bucket_name: str, object_name: str
) -> None:
    storage = BucketStorage()

    storage.init_object(bucket_name, object_name)
    ret = storage.get_object(bucket_name, object_name)

    assert ret
    assert ret["Body"].read().decode("utf-8") == ""

    s3_client.delete_object(Bucket=bucket_name, Key=object_name)


def test_init_returns_msg_that_object_already_is_in_bucket(
    bucket, s3_object, bucket_name: str, object_name: str
) -> None:
    storage = BucketStorage()

    ret = storage.init_object(bucket_name, object_name)

    assert ret
    assert (
        ret["Message"]
        == f"Object: {object_name} in bucket: {bucket_name} already exists!"
    )


def test_create_bucket(s3_client, bucket_name: str) -> None:
    storage = BucketStorage()
    ret = storage.create_bucket(bucket_name)

    assert (
        ret["Location"] == f"http://{bucket_name}.s3.localhost.localstack.cloud:4566/"
    )

    s3_client.delete_bucket(Bucket=bucket_name)


def test_create_bucket_raises_bucket_already_exists_error_on_existing_bucket(
    bucket, bucket_name: str
) -> None:
    storage = BucketStorage()

    with pytest.raises(BucketAlreadyExistsError):
        storage.create_bucket(bucket_name)


def test_create_bucket_raises_bucket_already_exists_error_on_existing_bucket_elsewhere(
    s3_client, bucket, bucket_name: str, mocker: MockerFixture
) -> None:
    p_mock = mocker.MagicMock(
        side_effect=s3_client.exceptions.BucketAlreadyExists({}, "Unknown")
    )
    storage = BucketStorage()
    storage.s3_client.create_bucket = p_mock

    with pytest.raises(BucketAlreadyExistsError):
        storage.create_bucket(bucket_name)


def test_add_quote_to_object_updates_object_content(
    bucket, s3_object, bucket_name: str, object_name: str
) -> None:
    storage = BucketStorage()

    before = storage.get_object(bucket_name, object_name)

    storage.add_quote_to_object(bucket_name, object_name, "some new quotation")

    after = storage.get_object(bucket_name, object_name)

    assert (
        after["Body"].read().decode("utf-8")
        == f"{before['Body'].read().decode('utf-8')}some new quotation\n"
    )


def test_add_quote_to_object_raises_object_does_not_exist(
    bucket, bucket_name: str, object_name: str
) -> None:
    storage = BucketStorage()

    with pytest.raises(ObjectNotFoundError):
        storage.add_quote_to_object(bucket_name, object_name, "some new quotation")


def test_add_quote_to_object_raises_bucket_does_not_exist(
    bucket_name: str, object_name: str
) -> None:
    storage = BucketStorage()

    with pytest.raises(BucketNotFoundError):
        storage.add_quote_to_object(bucket_name, object_name, "some new quotation")
