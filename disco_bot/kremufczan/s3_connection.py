import os
from typing import Any

import boto3

from .interface import QuotesStorageInterface


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
        return self.s3_client.get_object(Bucket=bucket_name, Key=key)

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
        except self.s3_client.exceptions.BucketAlreadyExists:
            return {"Message": "Bucket Already Exists!"}
        except self.s3_client.exceptions.BucketAlreadyOwnedByYou:
            return {"Message": "Bucket Already Owned By You!"}

    def add_quote_to_object(
        self, bucket_name: str, key: str, quote: str
    ) -> dict[str, Any]:
        try:
            curr_file = self.get_object(bucket_name, key)
        except self.s3_client.exceptions.NoSuchKey as e:
            raise e
        data = curr_file["Body"].read().decode("utf-8")
        new = f"{data}{quote}\n"

        return self.s3_client.put_object(Bucket=bucket_name, Key=key, Body=new)
