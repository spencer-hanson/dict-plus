from dict_plus import Element, Iterable, OrderedIterable, KeyValuePair
from dict_plus.exceptions import InvalidElementTypeException


class DictPlus(Iterable):
    pass


class OrderedDictPlus(OrderedIterable):
    def __init__(self, data=None, element_type=None, **kwargs):
        super(OrderedDictPlus, self).__init__(data, element_type or KeyValuePair, **kwargs)

    def __eq__(self, other):
        result = True

        if other == {} and self._elements == []:
            return True

        if not hasattr(other, "__len__") or len(other) != self.__len__():
            return False

        if isinstance(other, Iterable):
            for i in range(0, self.__len__()):
                if other._elements[i] != self._elements[i]:
                    result = False
                    break
            return result
        elif isinstance(other, dict):
            for el in self._elements:
                if el.id not in other:
                    result = False
                    break
                else:
                    result = result and el.value == other[el.id]
            return result
        else:
            return False

    # def __eq__(self, other):
    #     result = True
    #
    #     if (other == {} or other == []) and self._elements == []:
    #         return True
    #
    #     if not hasattr(other, "__len__") or len(other) != self.__len__():
    #         return False
    #
    #     if isinstance(other, Iterable):
    #         for i in range(0, self.__len__()):
    #             if other._elements[i] != self._elements[i]:
    #                 result = False
    #                 break
    #         return result
    #     elif isinstance(other, dict):
    #         for el in self._elements:
    #             if el.id not in other:
    #                 result = False
    #                 break
    #             else:
    #                 result = result and el.value == other[el.id]
    #         return result
    #     elif isinstance(other, list):
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
