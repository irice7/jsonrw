import utils

from typing import Any

from error import PossibleError

# FIXME: PossibleError doesn't work because of raised KeyError
class JsonStorage:
    def __init__(self, filename: str) -> None:
        self.json_dict: dict = utils.load_json(filename)
        self.index: dict = {}
        self.journal: dict = {}
        self.create_index()

    def create_index(self):
        for i, entry in enumerate(self.json_dict):
            for key, value in entry.items():
                if key not in self.index:
                    self.index[key] = {}
                self.index[key][f'{value}'] = i

    def get(self, key: str) -> Any:
        if key not in self.json_dict[0]:
            return PossibleError(True, f'Key {key} not in dictionary')

        return self.json_dict[0][key]

    def set(self, key: str):
        pass

class JsonDatabase:
    def __init__(self, filename: str) -> None:
        self.storage: JsonStorage = JsonStorage(filename)

    def query(self, key: str, value: Any) -> Any:
        if key not in self.storage.index and value not in self.storage.index[key]:
            return PossibleError(False, "Query fail")
        return (self.storage.json_dict[self.storage.index[key][value]])[key]

# remove test
if __name__ == '__main__':
    db = JsonDatabase('test.json')
    value = db.query('name', 'Bob')
    if isinstance(value, PossibleError):
        print(value.MESSAGE)
    print(value)
