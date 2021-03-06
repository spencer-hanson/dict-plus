from dict_plus.iterable import Iterable, OrderedIterable
from dict_plus.indexes import SortedIterableIndex


class OrderedDictPlus(OrderedIterable):
    def __init__(self, *args, **kwargs):
        """Create a new OrderedDictPlus, with inital data and element_type defaulting to KeyValuePair,
        and other keyword args to include in the dict upon creation

        Args:
            data: data to use initially in the OrderedDictPlus. Can be a tuple list or a dict, or an object with .keys()
            element_type: Element type to store the data with, defaults to KeyValuePair
            kwargs: keyword args to include in the dict

        """
        # self._elements_type = element_type or ElementFactory.element(KeyValuePair, OrderedDictPlus)
        super(OrderedDictPlus, self).__init__(*args, **kwargs)

    @staticmethod
    def fromkeys(sequence, value=None):
        """Create a new DictPlus from a sequence of keys, all with value 'value'

        Args:
            sequence: iterable of keys
            value: value to set each key to, defaults to None

        Returns:
            DictPlus with populated data

        """
        d = OrderedDictPlus()
        for item in sequence:
            d.insert(len(d), (item, value))
        return d

    def __eq__(self, other):
        """Check if self == other, for each key and value

        Args:
            other: Iterable-like to compare to

        Returns:
            Boolean True or False

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


class SortedDictPlus(OrderedDictPlus):
    def __init__(self, *args, **kwargs):
        # self._elements_type = element_type or ElementFactory.element(KeyValuePair, SortedDictPlus)
        super(SortedDictPlus, self).__init__(*args, **kwargs)

    def _make_index(self):
        """Make the internal index for the Dictionary, for custom indexing

        Returns:
            A subclass of IterableIndex

        """
        return SortedIterableIndex()

    @staticmethod
    def fromkeys(sequence, value=None):
        """Create a new DictPlus from a sequence of keys, all with value 'value'

        Args:
            sequence: iterable of keys
            value: value to set each key to, defaults to None

        Returns:
            DictPlus with populated data

        """
        d = SortedDictPlus()
        for item in sequence:
            d.insert(len(d), (item, value))
        return d

    def insert(self, index, obj):
        """Insert an object into the Iterable, raises a KeyError if the key already exists
        Index value is ignored in the Iterable superclass, as order is not preserved anyways

        Args:
            index: Value to insert element to, unless ordered, the index always will be the last
            obj: Object to insert into the Iterable. Must conform with the element type of the iterable

        Returns:
            Element that was inserted

        """
        element = self._elements_type(obj)
        if self._indexes.has(element.id):
            raise KeyError("Key '{}' already exists!".format(element.id))

        inserted = -1

        val = self._indexes.make_hash(element.id)
        if self._indexes.isempty():
            self._elements.insert(0, element)
            inserted = 0
        else:
            for i in range(len(self._elements)):
                item = self._elements[i]
                v = self._indexes.make_hash(item.id)
                if val < v:
                    self._elements.insert(i, element)
                    inserted = i
                    break
            if inserted == -1:
                self._elements.insert(len(self), element)
                inserted = len(self)

        self._indexes.set(element.id, inserted)
        self._insert_to_dict_memory(element)
        self._update_indexes(inserted)  # Make sure to update the indexes after inserting

        return element
