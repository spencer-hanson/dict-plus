from dict_plus.etypes import *
import zlib


class IterableIndex(object):
    """
    Index object to keep track of 'unhashable' types
    """

    def make_hash(self, o):
        """
        Makes a hash for a given object, doesn't guarantee collisions won't happen.
        :param o: Object to get a hash for
        :return: The hash of the object
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
        """
        :param data: Internal data dict to create the index from, optional
        """
        self.__data = {} if not data else data.copy()

    def get(self, key):
        """
        Get a value from the index
        :param key: Key to get the value of
        :return: Integer index of the key's location in the element list
        """
        key_hash = self.make_hash(key)
        if key_hash in self.__data:
            return self.__data[key_hash]
        else:
            raise KeyError("Key '{}' not in index ".format(key))

    def set(self, key, value):
        """
        Set a key's location in the index
        :param key: Key to get the location of
        :param value: Integer value to set in the index
        :return: None
        """
        if not isinstance(value, int):
            raise ValueError("Can't set index value to non-integer value!")

        self.__data[self.make_hash(key)] = value

    def has(self, key):
        """
        Check whether the index has a given key in it
        :param key: Key to check for
        :return: True if the key exists, else False
        """
        if self.make_hash(key) in self.__data:
            return True
        else:
            return False

    def pop(self, key):
        """
        Remove and get the value of the given key
        :param key: Key to get the value of
        :return: Integer index value of the key in the element list
        """
        return self.__data.pop(self.make_hash(key))

    def isempty(self):
        """
        Check whether the index is empty
        :return: True if index is empty else False
        """
        return self.__data == {}

    def copy(self):
        """
        Copy this index
        :return: A copy of the index
        """
        return self.__class__(self.__data)


class SortedIterableIndex(IterableIndex):
    """
    Index object to keep track of 'unhashable' types
    """
    def make_hash(self, o):
        """
        Makes a hash for a given object, doesn't guarantee collisions won't happen.
        :param o: Object to get a hash for
        :return: The hash of the object
        """

        if isinstance(o, StringTypes):
            if six.PY3:
                o = o.encode()

            return zlib.crc32(o) & 0xffffffff

        if isinstance(o, list):
            hashes = []
            for el in o:
                hashes.append(self.make_hash(el))
            return self.make_hash(str(hashes) + "l")
        elif isinstance(o, dict):
            return self.make_hash(o.items())
        elif isinstance(o, set):
            return self.make_hash(str(self.make_hash(list(o))) + "s")
        elif hasattr(o, "__str__"):
            return self.make_hash(str(o) + "_s")
        else:
            raise TypeError("Can't hash {}, submit an issue!".format(o))
