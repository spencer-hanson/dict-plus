from dict_plus.exceptions import *


class Iterable(object):  # TODO CHANGE ME TO dict after debug
    # __hash__ = None  # TODO ?

    def __init__(self, data=None, element_type=None, **kwargs):
        """
        dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)
        # (copied from class doc)
        """

        super().__init__()
        if not element_type:
            element_type = Element

        self._elements = []
        self._eltype = element_type
        self._indexes = {}

        if isinstance(data, dict):
            self.update(data)
        elif isinstance(data, list):
            for idx, el in enumerate(data):
                self.insert(len(self), (idx, el))
        elif data:
            for k, v in data:
                self.insert(len(self), (k, v))
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def _update_indexes(self, from_idx):  # TODO Use from_idx to optimize
        self._indexes = {}
        for idx, el in enumerate(self._elements):
            self._indexes[el.id] = idx

    def insert(self, index, obj):
        element = self._eltype(obj=obj)
        if element.id in self._indexes:
            raise KeyError("Key '{}' already exists!".format(element.id))

        self._elements.insert(len(self), element)  # Just add to the end of the iterable
        self._indexes[element.id] = len(self) - 1
        return element

    def get(self, k, v_alt=None):
        """ D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None. """
        return self.getitem(k, v_alt).value

    def getitem(self, k, v_alt=None):
        if k in self._indexes:
            return self._elements[self._indexes[k]]
        elif v_alt:
            return self._eltype(k, v_alt)
        else:
            raise KeyError("No key '{}' found!".format(k))

    def pop(self, k, v_alt=None):
        """
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        # Don't care about order, so we move the last element to the position of the removed
        # element, remove the index to the popped element
        if k in self._indexes:
            last_el = self._elements.pop(-1)
            el_idx = self._indexes[k]
            element = self._elements[el_idx]
            self._elements[el_idx] = last_el
            self._indexes[last_el.id] = el_idx
            self._indexes.pop(k)
            return element.value
        elif v_alt:
            return v_alt
        raise KeyError("Key '{}' not found!".format(k))

    def popitem(self):
        """
        D.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if D is empty.
        """
        if self._indexes == {}:
            raise KeyError("Can't .popitem, dict is empty!")
        k, v = self._elements.pop(-1).parts()
        self._indexes.pop(k)

        return k, v

    def unupdate(self, e=None, **kwargs):
        if hasattr(e, "keys"):
            for k in e.keys():
                if self.pop(k) != e[k]:
                    raise InvalidElementValueException
        else:
            for k, v in e:
                if self.pop(k) != v:
                    raise InvalidElementValueException
        for k in kwargs:
            if self.pop(k) != kwargs[k]:
                raise InvalidElementValueException

    def update(self, e=None, **kwargs):
        """
        D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
        If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
        In either case, this is followed by: for k in F:  D[k] = F[k]
        """
        if hasattr(e, "keys"):
            for k in e.keys():
                if k in self._indexes:
                    self[k] = e[k]
                else:
                    self.insert(len(self), (k, e[k]))
        else:
            for k, v in e:
                self.insert(len(self), (k, v))
        for k in kwargs:
            self.insert(len(self), (k, kwargs[k]))

    def map(self, func):
        for i in range(0, len(self)):
            idx = self._indexes.pop(self._elements[i].id)
            self._elements[i] = self._eltype(obj=func(*self._elements[i].parts()))
            self._indexes[self._elements[i].id] = idx

    def rekey(self, func):
        for i in range(0, len(self)):
            idx = self._indexes.pop(self._elements[i].id)
            self._elements[i].id = func(self._elements[i].id)
            self._indexes[self._elements[i].id] = idx

    def clear(self):
        """ D.clear() -> None.  Remove all items from D. """
        self._elements = []
        self._indexes = {}

    def copy(self):
        """ D.copy() -> a shallow copy of D """
        i = self.__class__(element_type=self._eltype)
        i._elements = self._elements.copy()
        i._indexes = self._indexes.copy()
        return i

    def atindex(self, int_val):
        return self.getitem(self._elements[int_val].id)

    @staticmethod
    def fromkeys(sequence, value=None):
        raise NotImplementedError("Can't call .fromkeys() on Iterator!")

    def items(self):
        """ D.items() -> a set-like object providing a view on D's items """
        return set([el.parts() for el in self._elements])

    def keys(self):
        """ D.keys() -> a set-like object providing a view on D's keys """
        return set([el.id for el in self._elements])

    def values(self):
        """ D.values() -> an object providing a view on D's values """
        return [el.value for el in self._elements]

    def setdefault(self, k, d=None):
        """ D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D """
        if k in self._indexes:
            return self._elements[self._indexes[k]]
        else:
            self[k] = d
            return d

    def todict(self):
        d = {}
        for el in self._elements:
            d[el.id] = el.value
        return d

    def swap(self, k1, k2):
        tmp_val = self._elements[self._indexes[k1]]
        self._elements[self._indexes[k1]] = self._elements[self._indexes[k2]]
        self._elements[self._indexes[k2]] = tmp_val

    def squish(self, keys, new_keys, func):
        a = [self.getitem(key) for key in keys]
        func(*a)
        tw = 2
        raise NotImplementedError

    # expand any number of keys into a larger amount of keypairs
    def expand(self, keys, func):
        raise NotImplementedError

    # TODO: Give default plus behavior, expected from adding two dicts together, d1+d2 = d1.update(d2)
    def plus(self, other, func=None):
        if not isinstance(other, Iterable):
            other = self.__init__(other)
        if not func:
            def func(e1, e2):
                self.insert(-1, e2)
                return e1
        for i in range(0, min(len(self), len(other))):
            ep = func(self._elements[i], other.atindex(i))
            self._elements[i] = self._eltype(obj=ep)
        return self

    # Same with minus TODO
    def minus(self, other, func_inv=None):
        raise NotImplementedError

    def chop(self, func):
        raise NotImplementedError

    def funcmap(self, f, g):
        raise NotImplementedError

    def fold_left(self, func):
        if len(self._elements) < 2:
            return self  # Can't fold unless we have at least 2 elements

        tmp_el = self._elements[0]
        for el in self._elements[1:]:
            result = func(tmp_el, el)
            tmp_el = self._eltype(obj=result)
        return tmp_el

    def fold_right(self, func):
        if len(self._elements) < 2:
            return self  # Can't fold unless we have at least 2 elements

        tmp_el = self._elements[-1]
        for idx in range(len(self._elements) - 1, 0, -1):
            result = func(tmp_el, self._elements[idx - 1])
            tmp_el = self._eltype(obj=result)
        return tmp_el

    def multiply(self, iterable, func):
        raise NotImplementedError

    def divide(self, iterable, func_inv):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    ##
    # @staticmethod  # known case of __new__
    # def __new__(*args, **kwargs):  # real signature unknown
    #     """ Create and return a new object.  See help(type) for accurate signature. """
    #     raise NotImplementedError
    #
    # def __contains__(self, *args, **kwargs):  # real signature unknown
    #     """ True if D has a key k, else False. """
    #     raise NotImplementedError
    #
    # def __delitem__(self, *args, **kwargs):  # real signature unknown
    #     """ Delete self[key]. """
    #     raise NotImplementedError
    #
    def __eq__(self, other):
        raise NotImplementedError("Can't equate Iterable instances!")

    def __add__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        raise NotImplementedError

    def __divmod__(self, other):  # TODO ???
        raise NotImplementedError

    #
    # def __getattribute__(self, *args, **kwargs):  # real signature unknown
    #     """ Return getattr(self, name). """
    #     raise NotImplementedError
    #

    # TODO: when checked for 'a in self', under 'object' superclass, it will call this method
    # TODO over and over with keys '0, 1, 2, ...' without bound?
    def __getitem__(self, k):
        """ x.__getitem__(y) <==> x[y] """
        return self.get(k)

    def __setitem__(self, key, value):
        """ Set self[key] to value. """
        if key in self._indexes:
            self._elements[self._indexes[key]].value = value
        else:
            self.insert(len(self), (key, value))

    #
    # def __ge__(self, *args, **kwargs):  # real signature unknown
    #     """ Return self>=value. """
    #     raise NotImplementedError
    #
    # def __gt__(self, *args, **kwargs):  # real signature unknown
    #     """ Return self>value. """
    #     raise NotImplementedError
    #
    # def __iter__(self, *args, **kwargs):  # real signature unknown
    #     """ Implement iter(self). """
    #     # raise NotImplementedError
    #     return super(Iterable, self).__iter__()
    #

    def __len__(self):  # real signature unknown
        return len(self._elements)

    #
    # def __le__(self, *args, **kwargs):  # real signature unknown
    #     """ Return self<=value. """
    #     raise NotImplementedError
    #
    # def __lt__(self, *args, **kwargs):  # real signature unknown
    #     """ Return self<value. """
    #     raise NotImplementedError
    #
    # def __ne__(self, *args, **kwargs):  # real signature unknown
    #     """ Return self!=value. """
    #     raise NotImplementedError
    #
    # def __repr__(self, *args, **kwargs):  # real signature unknown
    #     return super(Iterable, self).__repr__(*args, **kwargs)
    #     # raise NotImplementedError
    #
    def __str__(self):
        return str(self.todict())

    # def __sizeof__(self):
    #     """ D.__sizeof__() -> size of D in memory, in bytes """
    #     raise NotImplementedError

    # squish any number of keys into a smaller amount of keypairs
    # f = (e_list) -> (new_e_list)


class OrderedIterable(Iterable):

    def insert(self, index, obj):
        element = self._eltype(obj=obj)
        if element.id in self._indexes:
            raise KeyError("Key '{}' already exists!".format(element.id))

        self._elements.insert(index, element)
        self._update_indexes(index)
        return element

    def pop(self, k, v_alt=None):
        """
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        if k in self._indexes:
            idx = self._indexes[k]
            result = self._elements.pop(idx).value
            self._update_indexes(idx)
            return result
        elif v_alt:
            return v_alt
        raise KeyError("Key '{}' not found!".format(k))


class Element(object):
    def __init__(self, _id=None, value=None, obj=None):
        if obj:
            self.id, self.value = self.parse_object(obj)
        else:
            if _id is None or value is None:
                raise TypeError("Invalid args, must provide id and value or object")
            self.id = _id
            self.value = value

    # Parse stuff like ("a", 1) -> Element("a", 1)
    @staticmethod
    def parse_object(obj):
        raise NotImplementedError

    def parts(self):
        return self.id, self.value

    def __eq__(self, other):
        if isinstance(other, Element) and other.id == self.id and self.value == other.value:
            return True
        elif isinstance(other, tuple) and self.id == other[0] and self.value == other[1]:
            return True
        return False


class KeyValuePair(Element):
    @staticmethod
    def parse_object(obj):
        if isinstance(obj, KeyValuePair):
            return obj.id, obj.value
        if not isinstance(obj, tuple):
            raise InvalidElementTypeException("Invalid KeyPair object, must be a tuple")
        if len(obj) != 2:
            raise InvalidElementTypeException("Invalid KeyPair object, length must be 2")
        return obj[0], obj[1]

    def __eq__(self, other):
        if isinstance(other, dict) and len(other) == 1:
            k, v = list(other.items())[0]
            if k == self.id and v == self.value:
                return True
        return super(KeyValuePair, self).__eq__(other)
