from typing import Any
from jsonrw import JsonRW
from error import QueryError

class JsonStorage():
    def __init__(self, filename: str) -> None:
        self.json: JsonRW = JsonRW(filename)
        self.indexed_json: JsonRW = JsonRW()
        self._index_json() 

    def _index_json(self) -> None:
        for i, entry in enumerate(self.json):
            for key, value in entry.items():
                if key not in self.indexed_json: self.indexed_json.new_dict(key)
                self.indexed_json.put(f"{key}.{value}", i)

    def get_json(self) -> JsonRW:
        return self.json

    def get_indexer(self) -> JsonRW:
        return self.indexed_json

    def query(self, key: str, value: Any) -> Any:
        if js.get_indexer().get(f"{key}.{value}") is None:
            raise QueryError("Key not found or has not been indexed")
        else:
            return js.get_json().get(
                js.get_indexer().get(f"{key}.{value}")
            )[key]


if __name__ == "__main__":
    js = JsonStorage("test.json")

    try:
        result = js.query("name", "Jerom")
        print(result)
    except QueryError as e:
        print(e)

