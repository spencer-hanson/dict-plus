from dict_plus.iterable import Iterable
from dict_plus.elements import ElementFactory, ListElement

# TODO ListPlus!


class ListPlus(Iterable):
    def get_element_type(self):
        return ElementFactory.element(ListElement, self.__class__)

    def __init__(self, data=None):
        # todo
        super(ListPlus, self).__init__()

    @staticmethod
    def fromkeys(sequence, value=None):
        l = ListPlus()
        for s in sequence:
            l.insert(-1, s)
        return l

    def insert(self, index, obj):
        """Insert an object into the List, if the key already exists, bump all keys forward one index

        Args:
            index: Value to insert element to
            obj: Object to insert into the Iterable. Must conform with the element type of the iterable

        Returns:
            Element that was inserted

        """
        element = self._elements_type((index, obj))
        if self._indexes.has(element.id):
            # Todo
            raise KeyError("Key '{}' already exists!".format(element.id))

        self._elements.insert(len(self), element)  # Just add to the end of the iterable
        self._indexes.set(element.id, len(self) - 1)
        self._insert_to_dict_memory(element)
        return element