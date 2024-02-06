import utils
from typing import Any, Union, Self

class DictObj:
    def __init__(self, data: dict, root: "RootObj") -> None:
        self.data = data
        self.root = root

    def new_dict(self, key) -> "DictObj":
        self.data[key] = { }
        o = DictObj(self.data[key], self.root) 

        if self.root.auto_commit: self.root.save()
        return o

    def new_list(self, key) -> "ListObj":
        self.data[key] = [ ] 
        o = ListObj(self.data[key], self.root)

        if self.root.auto_commit: self.root.save()
        return o

    def put(self, key: str, value) -> "DictObj": 
        if len(key.split(".")) != 1: utils.parse_dot_separated_keys(self.data, key, value=value)
        else: self.data[key] = value
        if self.root.auto_commit: self.root.save()

        return self

    def get(self, key: str) -> Union[Self, "ListObj", Any, None]:
        if len(key.split(".")) != 1: o = utils.parse_dot_separated_keys(self.data, key)
        else: o = self.data[key]

        if isinstance(o, dict): return DictObj(o, self.root)
        elif isinstance(o, list): return ListObj(o, self.root)
        else: return o

    def __str__(self) -> str:
        return str(self.data)


class ListObj:
    def __init__(self, data: list, root: "RootObj") -> None:
        self.data = data
        self.root = root

    def new_dict(self, index: int = None) -> "DictObj":
        o = { }
        self.put(o, index=index)
        return DictObj(o, self.root)

    def new_list(self, index: int = None) -> Self:
        o = [ ]
        self.put(o, index=index)
        return ListObj(o, self.root)

    def put(self, value: object, index: int = None) -> "ListObj":
        if index == None: index = int(len(self.data))
        self.data.insert(index, value)
        if self.root.auto_commit: self.root.save()

        return self

    def get(self, index: int = None) -> Union["DictObj", Self, object, None]:
        o = self.data[index]
        if isinstance(o, dict): return DictObj(o, self.root)
        elif isinstance(o, list): return ListObj(o, self.root)
        else: return o 

    def __str__(self) -> str:
        return str(self.data)


class RootObj(DictObj):
    def __init__(self, data: dict, root: "JsonRW", auto_commit: bool = False) -> None:
        super().__init__(data, self)
        self.real_root = root
        self.auto_commit = auto_commit

    def save(self, indent: int = 4) -> None:
        self.real_root.save(indent=indent)

    def __str__(self) -> str:
        return str(self.data)


class JsonRW:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.root = RootObj(utils.load_json(filename), self)

    def new_dict(self, key: str) -> "DictObj":
        return self.root.new_dict(key)

    def new_list(self, key: str) -> "ListObj":
        return self.root.new_list(key)

    def put(self, key: str, value: str) -> None:
        self.root.put(key, value)

    def get(self, key: str) -> Union[Self, "ListObj", object, None]:
        return self.root.get(key)

    def save(self, **kwargs) -> None:
        utils.save_json(self.filename, self.root.data, **kwargs)

    def commit(self) -> None:
        self.root.commit()
         
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
   
