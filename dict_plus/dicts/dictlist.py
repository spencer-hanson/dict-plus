from dict_plus.dicts.dictplus import DictPlus


class DictList(DictPlus):
    def __init__(self, *args, **kwargs):
        """
        Create a new DictList a dictionary where each key is a list of values
        Args:
            data: data to use initially in the DictList. Can be a tuple list or a dict, or an object with .keys()
            element_type: Element type to store the data with, defaults to KeyValuePair
            kwargs: keyword args to include in the dict
        """
        super(DictList, self).__init__(*args, **kwargs)

    # TODO come up with funcs that would be useful here

