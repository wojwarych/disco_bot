from pathlib import Path
from typing import Any

from .interface import QuotesStorageInterface
from .s3_connection import BucketAlreadyExistsError, ObjectNotFoundError


class TXTStorage(QuotesStorageInterface):
    def __init__(self) -> None:
        try:
            path_dir = Path("~/.local/share/disco_bot/")
            path_dir.mkdir(mode=0o640, parents=True, exist_ok=False)
        except FileExistsError:
            pass

    def init_object(self, bucket_name: str, key: str) -> dict[str, Any]:
        try:
            path_dir = Path(f"~/.local/share/disco_bot/{bucket_name}")
            txt_file = path_dir / key
            txt_file.touch(mode=0o644, exist_ok=False)
        except FileExistsError:
            return {
                "Message": f"Object: {key} in filetree: {bucket_name} already exists!"
            }
        return {"Pathfile": txt_file}

    def get_object(self, bucket_name: str, key: str) -> dict[str, Any]:
        try:
            path = Path(f"~/.local/share/disco_bot/{bucket_name}/{key}")
            path.stat()
            return {"Body": path}
        except FileNotFoundError as e:
            raise ObjectNotFoundError(f"Object with key '{key}' not found!") from e

    def create_bucket(self, bucket_name: str) -> dict[str, str]:
        try:
            p = Path(f"~/.local/share/disco_bot/{bucket_name}")
            p.mkdir(mode=0o644)
        except FileExistsError as exc:
            raise BucketAlreadyExistsError(
                f"Bucket '{bucket_name}' already exists!"
            ) from exc
        return {"Bucket": "Ok"}

    def add_quote_to_object(
        self, bucket_name: str, key: str, quote: str
    ) -> dict[str, Any]:
        try:
            curr_file = self.get_object(bucket_name, key)
        except ObjectNotFoundError as e:
            raise e
        data = curr_file["Body"].read_text(encoding="utf-8")
        new = f"{data}{quote}\n"
        data += new
        curr_file["Body"].write_text(data, encoding="utf-8")

        return {"Msg": "OK"}
