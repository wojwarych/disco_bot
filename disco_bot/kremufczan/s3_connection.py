import os
from typing import Any

import boto3

from .interface import QuotesStorageInterface


class BucketNotFoundError(Exception): ...


class BucketAlreadyExistsError(Exception): ...


class ObjectNotFoundError(Exception): ...


class MockBucketStorage(QuotesStorageInterface):
    def __init__(self, data: dict[str, list[dict[str, Any]]] | None = None) -> None:
        if not data:
            self.data = {}
        else:
            self.data = data

    def get_object(self, bucket_name: str, key: str) -> dict[str, Any]:
        if bucket_name not in self.data:
            raise BucketNotFoundError(f"Bucket '{bucket_name}' not found!")
        ret = next((obj for obj in self.data[bucket_name] if key in obj), None)
        if not ret:
            raise ObjectNotFoundError(f"Object with key '{key}' not found!")
        return ret

    def create_bucket(self, bucket_name: str) -> dict[str, str]:
        if bucket_name not in self.data:
            self.data[bucket_name] = []
            return {"Location": bucket_name}
        raise BucketAlreadyExistsError(f"Bucket '{bucket_name}' already exists!")

    def init_object(self, bucket_name: str, key: str) -> dict[str, Any]:
        try:
            self.get_object(bucket_name, key)
        except BucketNotFoundError as e:
            raise e
        except ObjectNotFoundError:
            self.data[bucket_name].append({key: {}})
            return {"Message": "Created"}
        else:
            return {"Message": "Couldn't init object"}

    def add_quote_to_object(self, bucket_name: str, key: str, quote) -> dict[str, Any]:
        try:
            curr_data = self.get_object(bucket_name, key)
        except (BucketNotFoundError, ObjectNotFoundError) as e:
            raise e
        data = curr_data["Body"]
        new = f"{data}{quote}\n"
        data = new
        print(self.data)
        return {}


class BucketStorage(QuotesStorageInterface):
    def __init__(self) -> None:
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION_NAME"),
        )

    def get_object(self, bucket_name: str, key: str) -> dict[str, Any]:
        try:
            return self.s3_client.get_object(Bucket=bucket_name, Key=key)
        except self.s3_client.exceptions.NoSuchBucket as e:
            raise BucketNotFoundError(f"Bucket '{bucket_name}' not found!") from e
        except self.s3_client.exceptions.NoSuchKey as e:
            raise ObjectNotFoundError(f"Object with key '{key}' not found!") from e

    def init_object(self, bucket_name: str, key: str) -> dict[str, Any]:
        try:
            self.s3_client.get_object(Bucket=bucket_name, Key=key)
        except self.s3_client.exceptions.NoSuchKey:
            return self.s3_client.put_object(Bucket=bucket_name, Key=key, Body="")
        return {"Message": f"Object: {key} in bucket: {bucket_name} already exists!"}

    def create_bucket(self, bucket_name: str) -> dict[str, str]:
        try:
            return self.s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": os.getenv("AWS_REGION_NAME")
                },
            )
        except self.s3_client.exceptions.BucketAlreadyExists as exc:
            raise BucketAlreadyExistsError(
                f"Bucket '{bucket_name}' already exists!"
            ) from exc
        except self.s3_client.exceptions.BucketAlreadyOwnedByYou as exc:
            raise BucketAlreadyExistsError(
                f"Bucket '{bucket_name}' already owned by you!"
            ) from exc

    def add_quote_to_object(
        self, bucket_name: str, key: str, quote: str
    ) -> dict[str, Any]:
        try:
            curr_file = self.get_object(bucket_name, key)
        except BucketNotFoundError as e:
            raise e
        except ObjectNotFoundError as e:
            raise e
        data = curr_file["Body"].read().decode("utf-8")
        new = f"{data}{quote}\n"

        return self.s3_client.put_object(Bucket=bucket_name, Key=key, Body=new)
