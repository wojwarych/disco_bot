# pylint: disable=redefined-outer-name,unused-argument
import os
from collections.abc import Iterator

import boto3
import pytest
from dotenv import load_dotenv

import docker


@pytest.fixture(scope="session", autouse=True)
def environment() -> None:
    load_dotenv()


@pytest.fixture
def bucket_name() -> str:
    return "random-bucket"


@pytest.fixture
def object_name() -> str:
    return "some-file.txt"


@pytest.fixture(scope="session", autouse=True)
def localstack_container() -> Iterator[None]:
    client = docker.from_env()  # type: ignore[attr-defined]
    localstack = client.containers.run(
        "localstack/localstack:latest",
        environment={
            "SERVICES": "s3",
            "HOSTNAME": "localstack",
            "HOSTNAME_EXTERNAL": "localstack",
            "DEFAULT_REGION": "eu-central-1",
        },
        ports={"4566/tcp": "4566"},
        detach=True,
    )

    yield

    localstack.stop()


@pytest.fixture
def s3_client():
    s3_client = boto3.client(
        "s3",
        endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION_NAME"),
    )

    yield s3_client

    s3_client.close()


@pytest.fixture
def bucket(s3_client, bucket_name: str) -> Iterator[None]:
    s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": os.getenv("AWS_REGION_NAME")},
    )

    yield

    s3_client.delete_bucket(Bucket=bucket_name)


@pytest.fixture
def s3_object(
    s3_client, bucket: None, bucket_name: str, object_name: str
) -> Iterator[None]:
    s3_client.put_object(Bucket=bucket_name, Key=object_name, Body="some random data")

    yield

    s3_client.delete_object(Bucket=bucket_name, Key=object_name)
