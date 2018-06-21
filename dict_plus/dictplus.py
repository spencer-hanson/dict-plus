from dict_plus import Iterable, OrderedIterableMixin, KeyValuePair
from dict_plus.exceptions import InvalidElementTypeException


class DictPlus(Iterable):
    def __init__(self, data=None, element_type=None, **kwargs):
        super(DictPlus, self).__init__(data, element_type or KeyValuePair, **kwargs)

    @staticmethod
    def fromkeys(sequence, value=None):
        d = DictPlus()
        for item in sequence:
            d.insert(-1, (item, value))
        return d

    def __eq__(self, other):
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
        super(OrderedDictPlus, self).__init__(data, element_type or KeyValuePair, **kwargs)

    @staticmethod
    def fromkeys(sequence, value=None):
        d = OrderedDictPlus()
        for item in sequence:
            d.insert(-1, (item, value))
        return d

    def keys(self):
        return [el.id for el in self._elements]

    def __eq__(self, other):
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
