from dict_plus import Iterable, OrderedIterableMixin, KeyValuePair
from dict_plus.exceptions import InvalidElementTypeException


class DictPlus(Iterable):
    def __init__(self, data=None, element_type=None, **kwargs):
        """
        Create a new DictPlus
        Default element_type is KeyValuePair
        :param data: data to use initially in the DictPlus. Can be a tuple list or a dict, or an object with .keys()
        :param element_type: Element type to store the data with, defaults to KeyValuePair
        :param kwargs: keyword args to include in the dict
        """
        super(DictPlus, self).__init__(data, element_type or KeyValuePair, **kwargs)

    @staticmethod
    def fromkeys(sequence, value=None):
        """
        Create a new DictPlus from a sequence of keys, all with value 'value'
        :param sequence: iterable of keys
        :param value: value to set each key to, defaults to None
        :return: DictPlus with populated data
        """
        d = DictPlus()
        for item in sequence:
            d.insert(-1, (item, value))
        return d

    def __eq__(self, other):
        """
        Check if self == other, for each key and value
        :param other: Iterable-like to compare to
        :return: Boolean True or False
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


class OrderedDictPlus(OrderedIterableMixin):
    def __init__(self, data=None, element_type=None, **kwargs):
        """
        Create a new OrderedDictPlus, with inital data and element_type defaulting to KeyValuePair,
        and other keyword args to include in the dict upon creation
        :param data: data to use initially in the OrderedDictPlus. Can be a tuple list or a dict, or an object with .keys()
        :param element_type: Element type to store the data with, defaults to KeyValuePair
        :param kwargs: keyword args to include in the dict
        """
        super(OrderedDictPlus, self).__init__(data, element_type or KeyValuePair, **kwargs)

    @staticmethod
    def fromkeys(sequence, value=None):
        """
        Create a new DictPlus from a sequence of keys, all with value 'value'
        :param sequence: iterable of keys
        :param value: value to set each key to, defaults to None
        :return: DictPlus with populated data
        """
        d = OrderedDictPlus()
        for item in sequence:
            d.insert(len(d), (item, value))
        return d

    def __eq__(self, other):
        """
        Check if self == other, for each key and value
        :param other: Iterable-like to compare to
        :return: Boolean True or False
        """
        result = super(OrderedDictPlus, self).__eq__(other)
        if not result:
            return False

        if isinstance(other, Iterable):
            for i in range(0, self.__len__()):
                if other._elements[i] != self._elements[i]:
                    return False
        elif isinstance(other, list):
            return False
        return True

# TODO use for __eq__ in ListPlus
    # def __eq__(self, other):
    #     result = True
    #     if isinstance(other, list):
    #         for i in range(0, self.__len__()):
    #             idx = self._elements[i].id
    #             if not isinstance(idx, int):
    #                 result = False
    #                 break
    #             else:
    #                 if other[idx] != self._elements[i].value:
    #                     result = False
    #                     break
    #         return result
    #     else:
    #         return False
    #
