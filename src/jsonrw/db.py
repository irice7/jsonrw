from typing import Any
from json.storage import JsonStorage

class Database:
    def __init__(self, db_path: str) -> None:
        self.storage = JsonStorage(db_path)

    def get(self, index: str) -> Any:
        return self.storage.json.get(index)
    
    def get(self, key: str) -> Any:
        return self.storage.json.get(key)

    def put(self, key: str, value: object) -> None:
        self.storage.json.put(key, value)

    def put(self, index: int) -> None:
        self.storage.json.put(index)

    def query(self, key, value) -> Any:
        return self.storage.query(key, value)

    def commit(self) -> None:
        self.storage.save()

    def close(self) -> None:
        self.commit()
        del self
