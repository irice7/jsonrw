import utils
from typing import Any, Iterator, Self

class DictObj:
    def __init__(self, data: dict, root: "JsonRW") -> None:
        self.data: dict = data
        self.root: "JsonRW" = root

    def new_dict(self, key: str) -> "DictObj":
        self.data[key] = { }
        o = DictObj(self.data[key], self.root) 

        if self.root.auto_commit: self.root.save()
        return o

    def new_list(self, key: str) -> "ListObj":
        self.data[key] = [ ] 
        o = ListObj(self.data[key], self.root)

        if self.root.auto_commit: self.root.save()
        return o

    def put(self, key: str, value: Any) -> "DictObj": 
        if len(key.split(".")) != 1: utils.parse_dot_separated_keys(self.data, key, value=value)
        else: self.data[key] = value
        
        if self.root.auto_commit: self.root.save()
        return self

    def get(self, key: str) -> Self | "ListObj" | Any | None:
        if len(key.split(".")) != 1: o = utils.parse_dot_separated_keys(self.data, key)
        else: o = self.data[key]

        if isinstance(o, dict): return DictObj(o, self.root)
        elif isinstance(o, list): return ListObj(o, self.root)
        else: return o

    def __str__(self) -> str:
        return str(self.data)

    # Iterator methods
    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator:
        return iter(self.data.values())

    def __list__(self) -> list:
        return list(self.data.keys())

    # Dictionary compatibility methods
    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> dict:
        self.put(key, value)
        return self.data

    def __delitem__(self, key: str) -> Any:
        return self.data.pop(key)

    def __contains__(self, key: str) -> bool:
        return key in self.data

class ListObj:
    def __init__(self, data: list, root: "JsonRW") -> None:
        self.data: list = data
        self.root: "JsonRW" = root

    def new_dict(self, index: int = None) -> "DictObj":
        o = { }
        self.put(o, index=index)
        return DictObj(o, self.root)

    def new_list(self, index: int = None) -> Self:
        o = [ ]
        self.put(o, index=index)
        return ListObj(o, self.root)

    def put(self, value: Any, index: int = None) -> "ListObj":
        if index == None: index = int(len(self.data))
        self.data.insert(index, value)
        if self.root.auto_commit: self.root.save()

        return self

    def get(self, index: int = None) -> "DictObj" | Self | Any | None:
        o = self.data[index]
        if isinstance(o, dict): return DictObj(o, self.root)
        elif isinstance(o, list): return ListObj(o, self.root)
        else: return o 

    def __str__(self) -> str:
        return str(self.data)

    # Iterator methods
    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator:
        return iter(self.data)

    def __list__(self) -> list:
        return self.data

    # List compatibility methods
    def __getitem__(self, index: int) -> Any:
        return self.data[index]

    def __setitem__(self, index: int, value: Any) -> dict:
        self.put(value, index=index)

    def __delitem__(self, index: int) -> Any:
        return self.data.pop(index)

    def __contains__(self, value: Any) -> bool:
        return value in self.data


class JsonRW:
    def __init__(self, filename: str = None, auto_commit: bool = False) -> None:
        self.filename: str = filename
        self.auto_commit: bool = auto_commit
        self.data: dict = utils.load_json(filename)

        print(self.data)
        
        if isinstance(self.data, dict): self.root = DictObj(self.data, self)
        elif isinstance(self.data, list): self.root = ListObj(self.data, self)

        self._init_methods()

    def _init_methods(self) -> None:
        self.new_dict = self.root.new_dict
        self.new_list = self.root.new_list
        self.put = self.root.put
        self.get = self.root.get
    
    def commit(self) -> None:
        if self.filename is None: return
        utils.save_json(self.filename, self.root.data, indent=4)

    def __str__(self) -> str:
        return self.root.__str__()

    # Iterator methods
    def __len__(self) -> int:
        return self.root.__len__()

    def __iter__(self) -> Iterator:
        return self.root.__iter__()

    def __list__(self) -> list:
        return self.root.__list__()

    # List/Dict compatibility methods
    def __getitem__(self, o: str | int) -> Any:
        return self.root[o]

    def __setitem__(self, o: str | int, value: Any) -> None:
        self.root[o] = value

    def __delitem__(self, o: str | int) -> Any:
        return self.root.__delitem__(o)

    def __contains__(self, o: str | Any) -> bool:
        return self.root.__contains__(o)

        
def test() -> None:
    js = JsonRW("test.json")

    var = True
    varChained = True

    # Test 1
    print("Test 1: JsonRW.put('out.in.var', True)")
    try:
        js.put("out.in.var", True)
        print("Test 1: Success!")
    except KeyError:
        print("Test 1: Failed")

    print("Test 1.1: JsonRW.get('out.in.var') == True")
    if js.get("out.in.var") == var: print("Test 1.1: Success!")
    else: print("Test 2.1: Failed!")

    # Test 2
    print("Test 2: Put JsonRW.nd('in').nd('out').put('varChained', True)")
    try:
        js.new_dict("in").new_dict("out").put("varChained", True)
        print("Test 2: Success!")
    except KeyError:
        print("Test 2: Failed!")
    
    print("Test 2.1: Get JsonRW.get('in').get('out').get('varChained') == True")
    if js.get("in").get("out").get("varChained") == varChained: print("Test 2.1: Success!")
    else: print("Test 2.1: Failed!")

    js.save(indent=4)

if __name__ == "__main__":
    test()
   
