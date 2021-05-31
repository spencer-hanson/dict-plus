from dict_plus.iterable import Iterable
from dict_plus.elements import ElementFactory, ListElement
from dict_plus.indexes import NullIndex
from dict_plus.etypes import StringTypes, NoneVal


class ListPlus(Iterable):
    def get_element_type(self):
        """
        Return an Element type to use internally, for ListPlus it should be a ListElement
        Returns:
            classtype
        """
        return ElementFactory.element(ListElement, self.__class__)

    def __init__(self, data=None):
        """
        Create a new ListPlus instance
        Args:
            data: List like data
        """
        super(ListPlus, self).__init__(data)

    @staticmethod
    def fromkeys(sequence, value=None):
        """
        Static function to create a new instance from a sequence/iterable. Here for compatibility
        """
        l = ListPlus()
        for s in sequence:
            l.insert(-1, s)
        return l

    def append(self, obj):
        """
        Add an element to the end of the list
        Args:
            obj: object to add to the list

        Returns:
            self
        """
        self.insert(-1, obj)
        return self

    def getitem(self, idx, v_alt=NoneVal):
        """
        Get an item in the list
        Args:
            idx: Index to get the data from
            v_alt: Alternate value to retrieve if the specified index doesn't exist

        Returns:
            List value
        """
        if isinstance(idx, int) and v_alt is not NoneVal:
            if idx > len(self._elements):
                return v_alt
            else:
                return self._elements[idx]
        else:
            return self._elements[idx]  # Will most likely raise key error

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

    def pop(self, idx=-1, v_alt=NoneVal):
        """
        Remove and get the value of an object in the list
        Args:
            idx: Index to pop, defaults to last element
            v_alt: Optional alternate value to return if the element at the index does not exist

        Returns:
            List Data
        """
        if isinstance(idx, int) and v_alt is not NoneVal:
            if idx > len(self._elements):
                return v_alt
            else:
                return self._elements.pop(idx).value
        else:
            return self._elements.pop(idx).value  # Could raise error if index doesn't exist

    def popitem(self):
        """
        Pop off the end of the list
        Returns:
            List Item
        """
        if not self._elements:
            raise ValueError("Cannot popitem(), empty list!")
        v = self.pop()
        l = len(self)
        return l, v

    def atindex(self, int_val):
        """
        Return the item at the given index
        Args:
            int_val: integer index value

        Returns:
            List Value
        """
        return self._elements[int_val]

    def indexof(self, idx):
        """
        Dummmy function
        Args:
            idx: idx

        Returns:
            index
        """

        return idx

    def tolist(self):
        """
        Convert the ListPlus into a default python list
        Returns:
            python list of data
        """
        return [el.value for el in self._elements]

    def todict(self):
        """
        Convert this list into a dictionary with numerical indexes as keys
        Returns:
            dict
        """

        d = {}
        for idx, el in enumerate(self._elements):
            d[idx] = el.value
        return d

    def __contains__(self, item):
        """
        Returns True/False if the item is in the list
        Args:
            item: value

        Returns:
            boolean True False
        """

        for el in self._elements:
            if el.value == item:
                return True
        return False

    def __setitem__(self, idx, value):
        """
        Set a specific index to a value, must be integer index
        Args:
            idx: Index into the list to set
            value: Value to set in the list

        Returns:
            None
        """

        if isinstance(idx, int):
            self._elements[idx] = self.get_element_type()(value)
        else:
            raise KeyError("Invalid key type, must be int!")

    def __str__(self):
        """
        Get the string representation of this object, should be the same as str(list)
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
        """Get an iterable instance from I, similar to iter(list) iterates on the keys

        Returns:
            iter of the keys

        """
        return iter(self.values())

    def _make_index(self):
        """
        Make the internal index, not used in the List
        Returns:
            NullIndex()
        """
        return NullIndex()

    def _update_indexes(self, from_idx):
        # Disabled on ListPlus
        pass

    def _insert_to_dict_memory(self, element):
        # Disabled on ListPlus
        pass

    def _remove_from_dict_memory(self, key):
        # Disabled on ListPlus
        pass

    def _clear_dict_memory(self):
        # Disabled on ListPlus
        pass

    def _update_dict_memory(self):
        # Disabled on ListPlus
        pass
