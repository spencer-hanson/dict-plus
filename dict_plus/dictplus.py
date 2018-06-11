from dict_plus import Element, Iterable
from dict_plus.exceptions import InvalidElementTypeException


class DictPlus(Iterable):
    def insert(self, index, obj):
        element = self._eltype(obj=obj)
        if element.id in self._indexes:
            raise KeyError("Key '{}' already exists!".format(element.id))

        self._elements.insert(index, element)
        self._update_index()
        return element

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
