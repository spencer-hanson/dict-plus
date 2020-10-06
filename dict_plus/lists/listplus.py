from dict_plus.iterable import Iterable
from dict_plus.elements import ElementFactory, ListElement
from dict_plus.indexes import NullIndex
from dict_plus.etypes import StringTypes, NoneVal

# TODO ListPlus!
"""
Possible implementations

1. List as a new data type/linked list approach
would have to scrap the Iterable superclass on this one, using a linked-list as the internal data
structure.

pros:
easiest implementation

cons:
Basically a linked list implementation with dict-plus functions tacked on

2. List as a dictionary
Use an ordered index, then remove all key access such that it's internally managed so that
the index looks like [(0, val), ..., (n, val)] and when an element at index 'i' is inserted,
traverse 'i' elements down the index to insert it. Then would have to update the rest of the (n-i)
list elements to update the 'keys'

pros:
would reuse inherited functions

cons:
would be slow since index updates each time

3. Hybrid 
Index elements have no key, just a value.
Internal Index mapping would need to be circumvented

pros:
could possibly reuse code from inheritance
would be fast

cons:
complex implementation

"""


class ListPlus(Iterable):
    def get_element_type(self):
        return ElementFactory.element(ListElement, self.__class__)

    def __init__(self, data=None):
        super(ListPlus, self).__init__(data)

    @staticmethod
    def fromkeys(sequence, value=None):
        l = ListPlus()
        for s in sequence:
            l.insert(-1, s)
        return l

    def append(self, obj):
        element = self._elements_type(obj)
        self._elements.append(element)
        return self

    def getitem(self, k, v_alt=NoneVal):
        if isinstance(k, int) and v_alt is not NoneVal:
            if k > len(self._elements):
                return v_alt
            else:
                return self._elements[k]
        else:
            return self._elements[k]  # Will most likely raise key error

    def insert(self, index, obj):
        """Insert an object into the List, if the key already exists, bump all keys forward one index

        Args:
            index: Value to insert element to
            obj: Object to insert into the Iterable. Must conform with the element type of the iterable

        Returns:
            Element that was inserted

        """
        element = self._elements_type(obj)

        self._elements.insert(index, element)
        return element

    def pop(self, k=-1, v_alt=NoneVal):
        if isinstance(k, int) and v_alt is not NoneVal:
            if k > len(self._elements):
                return v_alt
            else:
                return self._elements.pop(k).value
        else:
            return self._elements.pop(k).value  # Could raise error if index doesn't exist

    def popitem(self):
        if not self._elements:
            raise ValueError("Cannot popitem(), empty list!")
        v = self.pop()
        l = len(self)
        return l, v

    def atindex(self, int_val):
        return self._elements[int_val]

    def indexof(self, key):
        raise NotImplementedError

    def tolist(self):
        return [el.value for el in self._elements]

    def todict(self):
        d = {}
        for idx, el in enumerate(self._elements):
            d[idx] = el.value
        return d

    def __contains__(self, item):
        for el in self._elements:
            if el.value == item:
                return True
        return False

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._elements[key] = self.get_element_type()(value)
        else:
            raise KeyError("Invalid key type, must be int!")

    def __str__(self):
        """Get the string representation of this object, should be the same as str(list)
        Except for Python2, where dictionary order is not preserved

        Returns:
            String representing this ListPlus

        """

        def type_repr(v):
            if isinstance(v, StringTypes):
                return "'{}'".format(v)
            else:
                return str(v)

        entries = []
        for el in self._elements:
            entries.append("{}".format(type_repr(el.value)))
        return "[" + ",".join(entries) + "]"

    def __iter__(self):
        """Get an iterable instance from I, similar to iter(dict) iterates on the keys

        Returns:
            iter of the keys

        """
        return iter(self.values())

    def _make_index(self):
        return NullIndex()

    def _update_indexes(self, from_idx):
        pass

    def _insert_to_dict_memory(self, element):
        pass

    def _remove_from_dict_memory(self, key):
        pass

    def _clear_dict_memory(self):
        pass

    def _update_dict_memory(self):
        pass


