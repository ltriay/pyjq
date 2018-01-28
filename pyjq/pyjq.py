

STOP = True


class TypesNotInSync(TypeError):
    pass


class StopInspection:
    pass


def return_value(value, ret):
    return value, STOP


def lookup(struc, struc_search, default=[]):
    ret = default

    if type(struc_search) is dict:
        if type(struc) is not dict:
            raise TypesNotInSync
        for key, value in struc_search.items():
            if key in struc:
                if issubclass(type(value), Inspect):
                    ret = value.get(struc[key], ret)
                else:
                    ret = lookup(struc[key], struc_search[key], ret)
    elif type(struc_search) in [str, int, float, complex, type(None)]:
        ret.append(struc_search)
    elif "__getitem__" in struc_search.__dir__():
        if "__getitem__" not in struc.__dir__():
            raise TypesNotInSync
        if len(struc_search) == 1:
            item = struc_search[0]
            for an_item in struc:
                if issubclass(type(item), Inspect):
                    ret = item.get(an_item, ret)
                else:
                    ret = lookup(an_item, item, ret)
        else:
            raise TypesNotInSync
    else:
        print(struc, struc_search)
        raise TypeError

    return ret


class Inspect:
    def get(self, value, ret):
        ret.append(value)
        return ret


# Alias to Inspect
CreateList = Inspect


class MapDict(Inspect):
    def __init__(self, to_map):
        self.map = to_map

    def get(self, value, ret):
        ret.append({k: v for k, v in zip(value, self.map)})
        return ret


class Caller:
    """Differ call of a callable"""
    def __init__(self, caller):
        self.caller = caller

    def get(self, *args, **kwargs):
        return self.caller(*args, **kwargs)


def a_callable(x, y):
    return x * y


SAMPLE = {"a1": [1, 2, 3]}
SEARCH = {"a1": CreateList()}

EXAMPLE = {"a": 1, "b": [{"c": ["i", "j"]}, {"d": {"o": ["p", "q"]}}, {"e": 8}], "k": 9, "l": {"m": 10},
           "n": (11, 12, 13), "r": [20, 21, 22], "f": "toto", "p": [1, 2]}
LOOKUP = {"b": [{"c": CreateList(), "d": CreateList()}], "l": CreateList(), "n": [CreateList()],
          "r": CreateList(), "f": "const", "p": MapDict(["a", "b"])}

print(lookup(EXAMPLE, LOOKUP))
