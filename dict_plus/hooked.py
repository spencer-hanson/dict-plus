from dict_plus import DictPlus, KeyValuePair


class HookedDictPlus(DictPlus):
    def __init__(self, data=None, element_type=None, hooks, **kwargs):
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
        super(HookedDictPlus, self).__init__(data, element_type or KeyValuePair, **kwargs)

    def setdefault(self, k, v_alt=None):
        k = self.hooks["get"]["key"](k)
        return self.hooks["get"]["value"](super().setdefault(k, v_alt))

    def __contains__(self, item):
        return super().__contains__(item)

    def indexof(self, key):
        return super().indexof(key)

    def update(self, e=None, **kwargs):
        super().update(e, **kwargs)

    def insert(self, index, obj):
        return super().insert(index, obj)

    def getitem(self, k, v_alt=None):
        return super().getitem(k, v_alt)

    def pop(self, k, v_alt=None):
        return super().pop(k, v_alt)

    def popitem(self):
        return super().popitem()

    def __setitem__(self, key, value):
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
