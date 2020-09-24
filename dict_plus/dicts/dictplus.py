from dict_plus.iterable import Iterable


class DictPlus(Iterable):
    def __init__(self, *args,  **kwargs):
        """Create a new DictPlus
        Default element_type is KeyValuePair

        Args:
            data: data to use initially in the DictPlus. Can be a tuple list or a dict, or an object with .keys()
            element_type: Element type to store the data with, defaults to KeyValuePair
            kwargs: keyword args to include in the dict

        """

        super(DictPlus, self).__init__(*args, **kwargs)

    @staticmethod
    def fromkeys(sequence, value=None):
        """Create a new DictPlus from a sequence of keys, all with value 'value'

        Args:
            sequence: iterable of keys
            value: value to set each key to, defaults to None

        Returns:
             DictPlus with populated data

        """
        d = DictPlus()
        for item in sequence:
            d.insert(-1, (item, value))
        return d

    def __eq__(self, other):
        """Check if self == other, for each key and value

        Args:
            other: Iterable-like to compare to

        Returns:
            Boolean True or False

        """
        result = super(DictPlus, self).__eq__(other)
        if not result:
            return False

        if isinstance(other, Iterable):
            checked = []
            for i in range(0, self.__len__()):
                for j in range(0, len(other)):
                    if j not in checked:
                        if self._elements[i] == other._elements[j]:
                            checked.append(j)
            if set(range(0, len(other))) != set(checked):
                return False
        elif isinstance(other, list):
            return False
        return True
