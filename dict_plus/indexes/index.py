class Index(object):
    """
    Index object to keep track of data internals
    """

    def make_hash(self, o):
        raise NotImplementedError

    def __init__(self, data=None):
        """Create a new Iterable Index

        Args:
            data: Internal data dict to create the index from, optional

        """
        self.__data = {} if not data else data.copy()

    def get(self, key):
        """Get a value from the index

        Args:
            key: Key to get the value of

        Returns:
            Integer index of the key's location in the element list

        """
        raise NotImplementedError

    def set(self, key, value):
        """Set a key's location in the index

        Args:
            key: Key to get the location of
            value: Integer value to set in the index

        """
        raise NotImplementedError

    def has(self, key):
        """Check whether the index has a given key in it

        Args:
            key: Key to check for

        Returns:
            True if the key exists, else False

        """
        raise NotImplementedError

    def pop(self, key):
        """ Remove and get the value of the given key

        Args:
            key: Key to get the value of

        Returns:
            Integer index value of the key in the element list

        """
        raise NotImplementedError

    def isempty(self):
        """Check whether the index is empty

        Returns:
            True if index is empty else False
        """
        raise NotImplementedError

    def copy(self):
        """Copy this index

        Returns:
            A copy of the index

        """
        raise NotImplementedError


class IterableIndex(Index):
    """Index object to keep track of 'unhashable' types
    """

    def make_hash(self, o):
        """Makes a hash for a given object, doesn't guarantee collisions won't happen.

        Args:
            o: Object to get a hash for

        Returns:
            The hash of the object

        """

        if o.__hash__:
            try:
                return hash(o)
            except TypeError:
                pass

        if isinstance(o, list):
            hashes = []
            for el in o:
                hashes.append(self.make_hash(el))
            return hash(str(hashes) + str(o.__class__))
        elif isinstance(o, dict):
            return self.make_hash(o.items())
        elif isinstance(o, set):
            return hash(str(self.make_hash(list(o))) + str(o.__class__))
        elif hasattr(o, "__str__"):
            return hash(str(o) + str(o.__class__))
        else:
            raise TypeError("Can't hash {}, submit an issue!".format(o))

    def __init__(self, data=None):
        """Create a new Iterable Index

        Args:
            data: Internal data dict to create the index from, optional

        """
        super(IterableIndex, self).__init__(data)
        self.__data = {} if not data else data.copy()

    def get(self, key):
        """Get a value from the index

        Args:
            key: Key to get the value of

        Returns:
            Integer index of the key's location in the element list

        """
        key_hash = self.make_hash(key)
        if key_hash in self.__data:
            return self.__data[key_hash]
        else:
            raise KeyError("Key '{}' not in index ".format(key))

    def set(self, key, value):
        """Set a key's location in the index

        Args:
            key: Key to get the location of
            value: Integer value to set in the index

        """
        if not isinstance(value, int):
            raise ValueError("Can't set index value to non-integer value!")

        self.__data[self.make_hash(key)] = value

    def has(self, key):
        """Check whether the index has a given key in it

        Args:
            key: Key to check for

        Returns:
            True if the key exists, else False

        """
        if self.make_hash(key) in self.__data:
            return True
        else:
            return False

    def pop(self, key):
        """ Remove and get the value of the given key

        Args:
            key: Key to get the value of

        Returns:
            Integer index value of the key in the element list

        """
        return self.__data.pop(self.make_hash(key))

    def isempty(self):
        """Check whether the index is empty

        Returns:
            True if index is empty else False
        """
        return self.__data == {}

    def copy(self):
        """Copy this index

        Returns:
            A copy of the index

        """
        return self.__class__(self.__data)


class NullIndex(Index):
    """
    Index that does nothing
    """
    def __init__(self, data=None):
        super(NullIndex, self).__init__()
        self.__data = None

    def make_hash(self, o):
        return 0

    def get(self, key):
        return None

    def set(self, key, value):
        pass

    def has(self, key):
        return False

    def pop(self, key):
        return None

    def isempty(self):
        return True

    def copy(self):
        return self.__class__(self.__data)
