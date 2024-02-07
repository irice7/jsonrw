from typing import Any
import json

def load_json(filename: str) -> dict: 
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, TypeError):
        return { } # Please dont raise FileNotFoundError again
        # We return an empty dictionary so even when the file 
        # doesnt exist we can still save it (basically an in-memory db temporarily)

def save_json(filename: str, data: dict, **kwargs) -> None:
    with open(filename, 'w') as file:
        json.dump(data, file, **kwargs)

def parse_dot_separated_keys(current: dict, keys: str, value: Any = None) -> Any | None:
    """ parse_dot_separated_keys
        Parses strings that is dot separated like -> "a.b.c"
        It then maps, for example "a.b.c" as a dictionary which looks like this -> { "a": { "b": { "c": ANY } } }
        
        Note:
            When value isn't set it will return the very last key else it will set key to the set value
            This will create the required dictionaries when it doesn't exist
        
        It either returns None or Any. Depends on where your key lands
    """

    keys = keys.split('.')
    for key in keys[:-1]:
        if key not in current:
            current[key] = { }
        elif not isinstance(current[key], dict):
            raise ValueError(f"Key '{key}' is not a dictionary")
        current = current[key]

    if value is not None:
        current[keys[-1]] = value
    else:
        return current.get(keys[-1])
