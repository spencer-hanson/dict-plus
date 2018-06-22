from dict_plus.exceptions import *
from dict_plus.funcs import Functions as dfuncs
import functools


class Iterable(object):  # TODO CHANGE ME TO dict after debug
    # __hash__ = None  # TODO ?

    class IterableIndex(object):
        """
        Index object to keep track of 'unhashable' types
        """

        def __make_hash(self, o):
            if o.__hash__:
                return hash(o)
            elif isinstance(o, list):
                hashes = []
                for el in o:
                    hashes.append(self.__make_hash(el))
                return hash(str(hashes) + str(o.__class__))
            elif isinstance(o, dict):
                return self.__make_hash(o.items())
            elif isinstance(o, set):
                return hash(str(self.__make_hash(list(o))) + str(o.__class__))
            elif hasattr(o, "__str__"):
                return hash(str(o) + str(o.__class__))
            else:
                raise TypeError("Can't hash, submit an issue!")

        def __init__(self, data=None):
            self.__data = {} if not data else data.copy()

        def get(self, key):
            key_hash = self.__make_hash(key)
            if key_hash in self.__data:
                return self.__data[key_hash]
            else:
                raise KeyError(" '{}' ".format(key))

        def set(self, key, value):
            self.__data[self.__make_hash(key)] = value

        def has(self, key):
            if self.__make_hash(key) in self.__data:
                return True
            else:
                return False

        def pop(self, key):
            return self.__data.pop(self.__make_hash(key))

        def isempty(self):
            return self.__data == {}

        def copy(self):
            return Iterable.IterableIndex(self.__data)

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
        if isinstance(data, Iterable):
            self._elements = data._elements.copy()
            self._indexes = data._indexes.copy()
            self._eltype = data._eltype
        else:
            if not element_type:
                element_type = Element

            self._elements = []
            self._eltype = element_type
            self._indexes = Iterable.IterableIndex()

            if isinstance(data, dict):
                self.update(data)
            elif isinstance(data, list):
                for idx, el in enumerate(data):
                    self.insert(len(self), el)
            elif data:
                for k, v in data:
                    self.insert(len(self), (k, v))
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    # TODO Use from_idx to optimize
    def _update_indexes(self, from_idx):
        self._indexes = Iterable.IterableIndex()
        for idx, el in enumerate(self._elements):
            self._indexes.set(el.id, idx)

    def insert(self, index, obj):
        element = self._eltype(obj)
        if self._indexes.has(element.id):
            raise KeyError("Key '{}' already exists!".format(element.id))

        self._elements.insert(len(self), element)  # Just add to the end of the iterable
        self._indexes.set(element.id, len(self) - 1)
        return element

    def get(self, k, v_alt=None):
        """ D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None. """
        return self.getitem(k, v_alt).value

    def getitem(self, k, v_alt=None):
        if self._indexes.has(k):
            return self._elements[self._indexes.get(k)]
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
        if self._indexes.has(k):
            last_el = self._elements.pop(-1)
            el_idx = self._indexes.get(k)
            if el_idx != len(self):
                element = self._elements[el_idx]
                self._elements[el_idx] = last_el
                self._indexes.set(last_el.id, el_idx)
            else:
                element = last_el
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
        if self._indexes.isempty():
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
                if self._indexes.has(k):
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
            self._elements[i] = self._eltype(func(*self._elements[i].parts()))
            self._indexes.set(self._elements[i].id, idx)

    def rekey(self, func):
        for i in range(0, len(self)):
            idx = self._indexes.pop(self._elements[i].id)
            self._elements[i].id = func(self._elements[i].id)
            self._indexes.set(self._elements[i].id, idx)

    def clear(self):
        """ D.clear() -> None.  Remove all items from D. """
        self._elements = []
        self._indexes = Iterable.IterableIndex()

    def copy(self):
        """ D.copy() -> a shallow copy of D """
        i = self.__class__(element_type=self._eltype)
        i._elements = [el.copy() for el in self.elements()]
        i._indexes = self._indexes.copy()
        return i

    def atindex(self, int_val):
        return self.getitem(self._elements[int_val].id)

    def indexof(self, key):
        return self._indexes.get(key)

    @staticmethod
    def fromkeys(sequence, value=None):
        raise NotImplementedError("Can't call .fromkeys() on Iterator!")

    def items(self):
        """ D.items() -> a set-like object providing a view on D's items """
        return set([el.parts() for el in self._elements])

    def elements(self):
        return self._elements.copy()

    def keys(self):
        """ D.keys() -> a set-like object providing a view on D's keys """
        return set([el.id for el in self._elements])

    def values(self):
        """ D.values() -> an object providing a view on D's values """
        return [el.value for el in self._elements]

    def setdefault(self, k, d=None):
        """ D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D """
        if self._indexes.has(k):
            return self._elements[self._indexes.get(k)]
        else:
            self[k] = d
            return d

    @staticmethod
    def getfunc(name, *args, **kwargs):
        def func(inst):
            return getattr(inst, name)(*args, **kwargs)

        return func

    def todict(self):
        return {el.id: el.value for el in self._elements}

    def tolist(self):
        return [el.parts() for el in self._elements]

    def swap(self, k1, k2):
        tmp_val = self._elements[self._indexes.get(k1)]
        self._elements[self._indexes.get(k1)] = self._elements[self._indexes.get(k2)]
        self._elements[self._indexes.get(k2)] = tmp_val

    def squish(self, keys, new_key, func):
        vals = []
        for key in keys:
            vals.append(self.pop(key))
        self.insert(len(self), (new_key, func(vals)))

    # expand any number of keys into a larger amount of keypairs
    def expand(self, key, new_keys, func_inv):
        vals = func_inv(self.pop(key))
        if len(vals) != len(new_keys):
            raise IndexError("Number of values returned from the function != number of keys given!")
        for idx in range(0, len(new_keys)):
            self.insert(len(self), (new_keys[idx], vals[idx]))

    def add(self, other, func=None):
        if not isinstance(other, Iterable):
            other = self.__class__(other)
        if not func:
            def func(e1, e2):
                self.insert(len(self), e2)
                return e1

        done = False
        it1 = iter(self.elements())
        it2 = iter(other.elements())

        while not done:
            try:
                el1 = next(it1)
                el2 = next(it2)
                elp = func(el1, el2)
                if elp:
                    elp = self._eltype(elp)
                    idx = self._indexes.pop(el1.id)
                    self._indexes.set(elp.id, idx)
                    self._elements[idx] = elp
            except StopIteration:
                done = True
        return self

    def sub(self, other, func_inv=None):
        if not isinstance(other, Iterable):
            other = self.__class__(other)
        if not func_inv:
            def func_inv(_, e2):
                if e2 != self.getitem(e2.id):
                    raise KeyError("Cannot pop '{}'".format(e2))
                self.pop(e2.id)
                return None  # Explicitly return None for example purposes
        return self.add(other, func_inv)

    def chop(self, func):
        chopped = []
        data = {}
        for el in self._elements:
            idx = func(el.id, el.value)
            if idx in data:
                data[idx][el.id] = el.value
            else:
                data[idx] = self.__class__({el.id: el.value})
        for k, v in data.items():
            chopped.insert(k, v)

        return chopped

    # Combine self and other with function 'comp' using mapping 'mapp'
    def funcmap(self, other, comp, mapp, inplace=True):
        if not isinstance(other, Iterable):
            other = self.__class__(other)

        if inplace:
            d = self
        else:
            d = self.copy()

        for idx in range(0, len(self)):
            el = d._elements[idx]
            val1 = el.value
            gval = mapp(el.id)
            val2 = other[gval]
            fval = comp(val1, val2)
            d._elements[idx].value = fval

        return d

    def fold_left(self, func):
        if len(self._elements) < 2:
            return self  # Can't fold unless we have at least 2 elements

        tmp_el = self._elements[0]
        for el in self._elements[1:]:
            result = func(tmp_el, el)
            tmp_el = self._eltype(result)
        return tmp_el

    def fold_right(self, func):
        if len(self._elements) < 2:
            return self  # Can't fold unless we have at least 2 elements

        tmp_el = self._elements[-1]
        for idx in range(len(self._elements) - 1, 0, -1):
            result = func(tmp_el, self._elements[idx - 1])
            tmp_el = self._eltype(result)
        return tmp_el

    def multiply(self, other, func=None):
        if not isinstance(other, Iterable):
            other = self.__class__(other)
        if not func:
            def func(e1, e2):
                return (e1.id, e2.id), (e1.value, e2.value)
        els = self._elements.copy()
        self.clear()
        for el1 in els:
            for el2 in other.elements():
                el3 = self._eltype(func(el1, el2))
                self[el3.id] = el3.value
        return self

    def divide(self, other, func_inv=None):
        if not isinstance(other, Iterable):
            other = self.__class__(other)
        if not func_inv:
            def func_inv(e1, e2):
                if e1.id[0] == e2.id:
                    return e1.id[1], e1.value[1]
                else:
                    return e1.id[0], e1.value[1]
        return self.multiply(other, func_inv)

    # Compare self to other using
    # comparison func 'comp'
    # aggregate func 'agg'
    # and mapping func 'mapp'

    def compare(self, other, comp, agg, mapp=None, inplace=False):
        if not mapp:
            def mapp(x):
                return other.atindex(self.indexof(x)).id

        result = self.funcmap(
            other=other,
            comp=comp,
            mapp=mapp,
            inplace=inplace
        )
        return agg(result)

    def __le__(self, other):
        agg = self.getfunc("fold_left", dfuncs.AND)
        return self.compare(other, dfuncs.LE, agg).value

    def __lt__(self, other):
        agg = self.getfunc("fold_left", dfuncs.AND)
        return self.compare(other, dfuncs.LT, agg).value

    def __ge__(self, other):
        agg = self.getfunc("fold_left", dfuncs.AND)
        return self.compare(other, dfuncs.GE, agg).value

    def __gt__(self, other):
        agg = self.getfunc("fold_left", dfuncs.AND)
        return self.compare(other, dfuncs.GT, agg).value

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
        if other == {} and self._elements == []:
            return True

        if not hasattr(other, "__len__") or len(other) != self.__len__():
            return False

        if isinstance(other, dict):
            for el in self._elements:
                if el.id not in other:
                    return False
                else:
                    if not el.value == other[el.id]:
                        return False
        return True

    def __add__(self, other):
        return self.copy().add(other, func=None)

    def __sub__(self, other):
        return self.copy().sub(other, func_inv=None)

    def __mul__(self, other):
        return self.copy().multiply(other, func=None)

    def __truediv__(self, other):
        return self.copy().divide(other, func_inv=None)

    #
    # def __getattribute__(self, *args, **kwargs):  # real signature unknown
    #     """ Return getattr(self, name). """
    #     raise NotImplementedError
    #

    def __iter__(self):
        return iter(self.keys())

    def __contains__(self, item):
        return self._indexes.has(item)

    def __getitem__(self, k):
        """ x.__getitem__(y) <==> x[y] """
        return self.get(k)

    def __setitem__(self, key, value):
        """ Set self[key] to value. """
        if self._indexes.has(key):
            self._elements[self._indexes.get(key)].value = value
        else:
            self.insert(len(self), (key, value))

    #
    # def __iter__(self, *args, **kwargs):  # real signature unknown
    #     """ Implement iter(self). """
    #     # raise NotImplementedError
    #     return super(Iterable, self).__iter__()
    #

    def __len__(self):
        return len(self._elements)

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


class OrderedIterableMixin(Iterable):

    def insert(self, index, obj):
        element = self._eltype(obj)
        if self._indexes.has(element.id):
            raise KeyError("Key '{}' already exists!".format(element.id))

        self._elements.insert(index, element)
        self._update_indexes(index)
        return element

    def pop(self, k, v_alt=None):
        """
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        if self._indexes.has(k):
            idx = self._indexes.get(k)
            result = self._elements.pop(idx).value
            self._update_indexes(idx)
            return result
        elif v_alt:
            return v_alt
        raise KeyError("Key '{}' not found!".format(k))


class Element(object):
    def __init__(self, _id=None, value=None):
        if _id and not value:
            self.id, self.value = self.parse_object(_id)
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

    def __str__(self):
        return "<{}, {}>".format(self.id, self.value)

    def copy(self):
        return self.__class__(self.id, self.value)


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
