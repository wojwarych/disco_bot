from abc import ABC, abstractmethod
from typing import Any


class QuotesStorageInterface(ABC):
    @abstractmethod
    def get_object(self, bucket_name: str, key: str) -> dict[str, Any]: ...

    @abstractmethod
    def create_bucket(self, bucket_name: str) -> dict[str, str]: ...

    @abstractmethod
    def init_object(self, bucket_name, key) -> dict[str, Any]: ...

    @abstractmethod
    def add_quote_to_object(self, bucket_name, key, quote: str) -> dict[str, Any]: ...
