from typing import Any, Union
import json

def load_json(filename: str) -> dict:
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return { }

def save_json(filename: str, data: dict, **kwargs) -> None:
    with open(filename, 'w') as file:
        json.dump(data, file, **kwargs)

def parse_dot_separated_keys(current: dict, keys: str, value: Any = None) -> Union[object, None]:
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
