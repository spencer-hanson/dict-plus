from dict_plus.indexes.index import IterableIndex
from dict_plus.etypes import *
import zlib


class SortedIterableIndex(IterableIndex):
    """Index object to keep track of 'unhashable' types
    """
    def make_hash(self, o):
        """Makes a hash for a given object, doesn't guarantee collisions won't happen.

        Args:
            o: Object to get a hash for

        Returns:
            The hash of the object

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
