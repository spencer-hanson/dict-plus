import math


class SimpleFlattener(object):
    """
    Utility class to flatten simple dictionaries into a top-level only dict
    e.g.
    {"a": {"a1": 1, "a2": 2}, "b": {"b1": 3, "b2": 4}}
    would flatten to
    {"a_a1": 1, "a_a2": 2, "b_b1": 3, "b_b2": 4}

    Not meant to be a general dictionary flattener TODO?
    """

    class _SimpleListType(object):
        """
        Helper class to distinguish a 'Simple List' a list of simple typed data
        """
        def __init__(self, val):
            self.val = val

    def __init__(self, simple_types=[], maxdepth=math.inf, delimiter="_", dict_types=[]):
        """
        simple_types is a list of types that should be treated as simple, base cases
        maxdepth is the maximum depth within the data to traverse, defaults to no maximum
        delimiter is the string used to separate subkeys in the flattened dict
        dict_types are types that should be treated as a dict
        """
        self.simple_types = {str, bytes, int, float, bool, tuple}
        for s in simple_types:
            self.simple_types.add(s)
        self.max_depth = maxdepth
        self.delimiter = delimiter
        self.dict_types = {dict}
        for d in dict_types:
            self.dict_types.add(d)

    def is_simplelist(self, val):
        """
        Check if a list is only of simple_types and also not mixed types
        """
        if isinstance(val, list):
            list_types = set()
            for element in val:
                list_types.add(type(element))
            if len(list_types) == 1:  # Only one type of element in the list
                if list_types.pop() in self.simple_types:
                    return True
            return False  # Multiple types of data within the list, or data is not simple
        else:
            return False

    def flatten(self, data, current_depth=0, key_prefix=""):
        if key_prefix:
            key_prefix = f"{key_prefix}{self.delimiter}"

        if current_depth > self.max_depth:
            return {key_prefix: data}

        if type(data) in self.dict_types:
            newdict = {}
            for key, val in data.items():
                new_keyprefix = f"{key_prefix}{key}"
                if type(val) in self.simple_types:
                    newdict[new_keyprefix] = val
                else:
                    newdict.update(self.flatten(val, current_depth=current_depth+1, key_prefix=new_keyprefix))
            return newdict
        elif isinstance(data, list):
            if self.is_simplelist(data):
                return {key_prefix: data}

        raise ValueError(f"SimpleFlatten cannot flatten data: '{data}'")
