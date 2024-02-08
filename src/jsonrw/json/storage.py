from typing import Any
from jsonrw import JsonRW, ListObj
from error import QueryError

class JsonStorage():
    def __init__(self, filename: str, index_path: str = None) -> None:
        self.json: JsonRW = JsonRW(filename)
        self.indexed_json: JsonRW = None

        if isinstance(self.json.root, ListObj):
            self.indexed_json = JsonRW(index_path)
            self.index_json() 

    def index_json(self) -> None:
        for i, entry in enumerate(self.json):
            for key, value in entry.items():
                if key not in self.indexed_json: self.indexed_json.new_dict(key)
                try:
                    if value in self.indexed_json[key]: continue
                except TypeError: print("h")

                self.indexed_json.put(f"{key}.{value}", i)

        self.indexed_json.save()

    def get_json(self) -> JsonRW:
        return self.json

    def get_indexed_json(self) -> JsonRW:
        return self.indexed_json

    def query(self, key: str, value: Any = None) -> Any:
        if self.indexed_json is None:
            return js.get_json().get(key)
        else:
            target_index = js.get_indexed_json().get(f"{key}.{value}") 
            if target_index is None: raise QueryError("Key not found or has not been indexed")
            else: return js.get_json().get(target_index)[key]

    def save(self) -> None:
        self.json.save()
        self.indexed_json.save()

if __name__ == "__main__":
    js = JsonStorage("test.json", "indexed.json")

    try:
        result = js.query("name", "Jerome")
        js.json.new_dict().put("Jerome", 69).new_dict('age').put("Uejejduud", 69420)
        
        js.save()
        js.index_json()

        print(result)
    except QueryError as e:
        print(e)

