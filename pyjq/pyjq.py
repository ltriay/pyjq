

STOP = True


class TypesNotInSync(TypeError):
    pass


class StopInspection:
    pass


def return_value(value, ret):
    return value, STOP


def lookup(struc, struc_search, default=[]):
    ret = default

    if type(struc) is not type(struc_search):
        raise TypesNotInSync

    if type(struc_search) is dict:
        for key, value in struc_search.items():
            if key in struc:
                if issubclass(Inspect, type(value)):
                    ret = value.get(struc[key], ret)
                else:
                    ret = lookup(struc[key], struc_search[key], ret)
    elif type(struc) is list:
        if len(struc_search) == 1:
            item = struc_search[0]
            for an_item in struc:
                if issubclass(Inspect, type(item)):
                    ret = item.get(an_item, ret)
                else:
                    ret = lookup(an_item, item, ret)
        else:
            raise TypesNotInSync
    else:
        raise TypeError

    return ret


class Inspect:
    def __init__(self, sub_listed=None):
        self.sub_listed = sub_listed

    def get(self, value, ret):
        ret.append(value)
        return ret


# Alias to Inspect
CreateList = Inspect


class CreateDict(Inspect):
    def __init__(self, sub_dir=None, sub_values=None):
        self.sub_dir = sub_dir
        self.sub_values = sub_values

    def get(self, value, ret):
        pass


EXAMPLE = {"a": 1, "b": [{"c": ["i", "j"]}, {"d": {"o": ["p", "q"]}}, {"e": 8}], "k": 9, "l": {"m": 10},
           "n": [11, 12, 13], "r": [20, 21, 22]}

LOOKUP = {"b": [{"c": Inspect(), "d": Inspect()}], "l": Inspect(), "n": [Inspect()],
          "r": Inspect([Inspect()])}

print(LOOKUP)

print(lookup(EXAMPLE, LOOKUP))
