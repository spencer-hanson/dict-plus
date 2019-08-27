from dict_plus import DictPlus, KeyValuePair, ElementFactory


class HookedDictPlus(DictPlus):
    def __init__(self, data=None, element_type=None, hooks=None, **kwargs):
        """
        Create a new HookedDictPlus
        Default element_type is KeyValuePair
        :param data: data to use initially in the HookedDictPlus. Can be a tuple list or a dict, or an object with .keys()
        :param element_type: Element type to store the data with, defaults to KeyValuePair
        :param kwargs: keyword args to include in the dict
        """
        self.hooks = hooks
        self.hooks = {
            "set": {
                "key": lambda x: x,
                "value": lambda x: x
            },
            "get": {
                "key": lambda x: x,
                "value": lambda x: x
            },
            "delete": {
                "key": lambda x: x,
                "value": lambda x: x
            },
            "insert": {
                "key": lambda x: x,
                "value": lambda x: x
            }
        }
        super(HookedDictPlus, self).__init__(data, element_type or ElementFactory.element(KeyValuePair, HookedDictPlus), **kwargs)

    def setdefault(self, k, v_alt=None):
        raise NotImplementedError
        k = self.hooks["get"]["key"](k)
        return self.hooks["get"]["value"](super().setdefault(k, v_alt))

    def __contains__(self, item):
        return super().__contains__(item)

    def indexof(self, key):
        raise NotImplementedError
        return super().indexof(key)

    def update(self, e=None, **kwargs):
        raise NotImplementedError
        super().update(e, **kwargs)

    def insert(self, index, obj):
        raise NotImplementedError
        return super().insert(index, obj)

    def getitem(self, k, v_alt=None):
        raise NotImplementedError
        return super().getitem(k, v_alt)

    def pop(self, k, v_alt=None):
        raise NotImplementedError
        return super().pop(k, v_alt)

    def popitem(self):
        raise NotImplementedError
        return super().popitem()

    def __setitem__(self, key, value):
        raise NotImplementedError
        super().__setitem__(key, value)

    @staticmethod
    def fromkeys(sequence, value=None):
        """
        Create a new DictPlus from a sequence of keys, all with value 'value'
        :param sequence: iterable of keys
        :param value: value to set each key to, defaults to None
        :return: DictPlus with populated data
        """
        d = HookedDictPlus()
        for item in sequence:
            d.insert(-1, (item, value))
        return d


class FunctionDictPlus(HookedDictPlus):

    def __init__(self, data=None, element_type=None, func=None, **kwargs):
        """
        Create a new HookedDictPlus
        Default element_type is KeyValuePair
        :param data: data to use initially in the HookedDictPlus. Can be a tuple list or a dict, or an object with .keys()
        :param element_type: Element type to store the data with, defaults to KeyValuePair
        :param kwargs: keyword args to include in the dict
        """
        def error_out(inp):
            raise ValueError("Can't do that on a FunctionDictPlus!")
        hooks = {
            "set": {
                "key": error_out,
                "value": error_out
            },
            "get": {
                "key": lambda x: x,
                "value": func
            },
            "delete": {
                "key": error_out,
                "value": error_out
            },
            "insert": {
                "key": error_out,
                "value": error_out
            }
        }
        super(FunctionDictPlus, self).__init__(data, element_type or ElementFactory.element(KeyValuePair, DictPlus), hooks, **kwargs)

    @staticmethod
    def fromkeys(sequence, value=None):
        raise ValueError("Can't create a FunctionDictPlus from keys!")


class TwoWayDictPlus(DictPlus):
    pass
