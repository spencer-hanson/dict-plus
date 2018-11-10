from dict_plus.exceptions import *
from dict_plus.funcs import Functions as DFuncs


class Iterable(object):
    # __hash__ = None  # TODO ?

    class IterableIndex(object):
        """
        Index object to keep track of 'unhashable' types
        """

        def __make_hash(self, o):
            """
            Makes a hash for a given object, doesn't guarantee collisions won't happen.
            :param o: Object to get a hash for
            :return: The hash of the object
            """
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
            key_hash = self.__make_hash(key)
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

            self.__data[self.__make_hash(key)] = value

        def has(self, key):
            """
            Check whether the index has a given key in it
            :param key: Key to check for
            :return: True if the key exists, else False
            """
            if self.__make_hash(key) in self.__data:
                return True
            else:
                return False

        def pop(self, key):
            """
            Remove and get the value of the given key
            :param key: Key to get the value of
            :return: Integer index value of the key in the element list
            """
            return self.__data.pop(self.__make_hash(key))

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
            return Iterable.IterableIndex(self.__data)

    def __init__(self, data=None, element_type=None, **kwargs):
        """
        Initialize a new Iterable

        Iterable() -> new empty Iterable
        Iterable(mapping) -> new Iterable initialized from a mapping object's
            (key, value) pairs
        Iterable(iterable) -> new Iterable initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        Iterable(**kwargs) -> new Iterable initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)

        :param data: Optional data to be inserted into the Iterable, can be a dict, list of tuples,
        or another Iterable instance
        :param element_type: Element container for the data, must inherit from Element
        Contains an id and a value
        :param kwargs: Additional data to initialize with
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
        """
        Update the internal index after an operation that messes with the index
        Not meant to be used after every operation, as it completely reinitializes the index from
        a given spot
        :param from_idx: Parameter to help make the re-indexing faster, will only update the indexes after
        from_idx, as to not have to update any index < from_idx
        :return: None
        """
        self._indexes = Iterable.IterableIndex()
        for idx, el in enumerate(self._elements):
            self._indexes.set(el.id, idx)

    def insert(self, index, obj):
        """
        Insert an object into the Iterable, raises a KeyError if the key already exists
        Index value is ignored in the Iterable superclass, as order is not preserved anyways
        :param index: Value to insert element to, unless ordered, the index always will be the last
        :param obj: Object to insert into the Iterable. Must conform with the element type of the iterable
        :return: Element that was inserted
        """
        element = self._eltype(obj)
        if self._indexes.has(element.id):
            raise KeyError("Key '{}' already exists!".format(element.id))

        self._elements.insert(len(self), element)  # Just add to the end of the iterable
        self._indexes.set(element.id, len(self) - 1)
        return element

    def get(self, k, v_alt=None):
        """
        I.get(k[, v_alt]) -> I[k] if k in I, else v_alt.
        v_alt defaults to None.
        If no such key is found, will throw a KeyError
        :param k: key to get the value of
        :param v_alt: alternate value to return if key doesn't exist
        :return: The value stored with the key
        """
        return self.getitem(k, v_alt).value

    def getitem(self, k, v_alt=None):
        """
        Get the full element from key 'k'
        if no key or value is present, Element(k, v_alt) will be returned
        :param k:
        :param v_alt:
        :return: Element with key 'k'
        """
        if self._indexes.has(k):
            return self._elements[self._indexes.get(k)]
        elif v_alt:
            return self._eltype(k, v_alt)
        else:
            raise KeyError("No key '{}' found!".format(k))

    def pop(self, k, v_alt=None):
        """
        Don't care about order, so we move the last element to the position of the removed
        element, remove the index to the popped element, to keep the time complexity constant

        I.pop(k[,v_alt]) -> v, remove specified key and return the corresponding value.
        If key is not found, v_alt is returned if given, otherwise KeyError is raised
        :param k: key to pop
        :param v_alt: alternate value if k doesn't exist
        :return: The retrieved value from key k
        """
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
        I.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if I is empty.
        Pops from the last index
        :return: (key, value)
        """
        if self._indexes.isempty():
            raise KeyError("Can't .popitem, dict is empty!")
        k, v = self._elements.pop(-1).parts()
        self._indexes.pop(k)
        return k, v

    def unupdate(self, e=None, **kwargs):
        """
        Undo a .update operation, essentially the same as popping a list of keys,
        except will raise an InvalidElementValueException if the key-value pair doesn't match what is to be popped

        :param e: dict or iterable to unupdate with
        :param kwargs: keyword args to unupdate from
        :return: None
        """
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
        I.update([E, ]**F) -> None.  Update I from dict/iterable E and F.
        If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
        If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
        In either case, this is followed by: for k in F:  D[k] = F[k]

        :param e: iterable/dict to update from
        :param kwargs: other keyword args to update from
        :return: None
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
        """
        Map each element in the Iterable to another using function 'func'
        :param func: func(key, value) -> (new_key, new_value)
        :return: None
        """
        for i in range(0, len(self)):
            idx = self._indexes.pop(self._elements[i].id)
            self._elements[i] = self._eltype(func(*self._elements[i].parts()))
            self._indexes.set(self._elements[i].id, idx)

    def rekey(self, func):
        """
        Re-key the Iterable with function 'func'
        Changes keys in place, values untouched
        :param func: func(key1) -> key2
        :return: None
        """
        for i in range(0, len(self)):
            idx = self._indexes.pop(self._elements[i].id)
            self._elements[i].id = func(self._elements[i].id)
            self._indexes.set(self._elements[i].id, idx)

    def clear(self):
        """
        I.clear() -> None.  Remove all items from I.
        :return: None
        """
        self._elements = []
        self._indexes = Iterable.IterableIndex()

    def copy(self):
        """
        I.copy() -> a shallow copy of I
        :return: Copied instance
        """
        i = self.__class__(element_type=self._eltype)
        i._elements = [el.copy() for el in self.elements()]
        i._indexes = self._indexes.copy()
        return i

    def atindex(self, int_val):
        """
        Get the element at index 'int_val'
        :param int_val: Integer value to fetch the element from
        :return: Element instance
        """
        return self.getitem(self._elements[int_val].id)

    def indexof(self, key):
        """
        Get the integer index value of a given key
        raises KeyError if key doesn't exist
        :param key: Key to get the index of
        :return: Integer index
        """
        return self._indexes.get(key)

    @staticmethod
    def fromkeys(sequence, value=None):
        """
        Create an Iterable instance using a list, each element will be used as a key,
        with each with value 'value'
        :param sequence: List of keys to use
        :param value: Value to set for each key
        :return: Instance with keys from 'sequence' with value 'value'
        """
        raise NotImplementedError("Can't call .fromkeys() on Iterator!")

    def items(self):
        """
        Returns a list of the items in the Iterable instance, in form (key, value)
        :return: a list providing a view on I's items
        """
        return [el.parts() for el in self._elements]

    def elements(self):
        """
        Returns a copy of the elements in the Iterable instance
        :return: List of Elements
        """
        return self._elements.copy()

    def keys(self):
        """
        A list providing a view on I's keys
        :return: List of keys in I
        """
        return [el.id for el in self._elements]

    def values(self):
        """
        I.values() -> an object providing a view on I's values
        :return: List of values in I
        """
        return [el.value for el in self._elements]

    def setdefault(self, k, v_alt=None):
        """
        Same as I.get(k,d), also set I[k]=d if k not in I
        :param k: key to use
        :param v_alt: Alternate value to set and return if k isn't in I
        :return: Element value
        """
        if self._indexes.has(k):
            return self._elements[self._indexes.get(k)]
        else:
            self[k] = v_alt
            return v_alt

    @staticmethod
    def getfunc(name, *args, **kwargs):
        """
        Get a wrapped static version of an Iterable function, with signature func(inst)
        Providing arguments and keyword arguments for the function.

        :param name: Name of the function to get
        :param args: Arguments to use for the function
        :param kwargs: Keyword arguments to use for the function
        :return: A function with signature f(instance)
        """
        def func(inst):
            return getattr(inst, name)(*args, **kwargs)

        return func

    def todict(self):
        """
        Convert the Iterable to a pure python dictionary
        :return: dict
        """
        return {el.id: el.value for el in self._elements}

    def tolist(self):
        """
        Convert the Iterable to a pure python list
        :return: list
        """
        return [el.parts() for el in self._elements]

    def swap(self, k1, k2):
        """
        Swap two keys in the Iterable, works in place
        :param k1: first key
        :param k2: second key
        :return: None
        """
        tmp_val = self._elements[self._indexes.get(k1)]
        self._elements[self._indexes.get(k1)] = self._elements[self._indexes.get(k2)]
        self._elements[self._indexes.get(k2)] = tmp_val

    def squish(self, keys, new_key, func):
        """
        Squish elements into another new element, using function 'func'
        Works in place.
        :param keys: List of keys to squish
        :param new_key: Name of the new key
        :param func: func([value1, value2, ...]) -> new_value
        :return: None
        """
        vals = []
        for key in keys:
            vals.append(self.pop(key))
        self.insert(len(self), (new_key, func(vals)))

    def expand(self, key, new_keys, func_inv):
        """
        Expand a key into a larger amount of keys
        Works in place
        :param key: Key to expand on
        :param new_keys: List of keys that will be set
        :param func_inv: func(value) -> [value1, value2, ..]
        :return: None
        """
        vals = func_inv(self.pop(key))
        if len(vals) != len(new_keys):
            raise IndexError("Number of values returned from the function != number of keys given!")
        for idx in range(0, len(new_keys)):
            self.insert(len(self), (new_keys[idx], vals[idx]))

    def add(self, other, func=None):
        """
        Add this Iterable with another Iterable-like
        combine with function 'func'
        If no function is given, the default function will concatenate the two Iterables
        Works in place, allows for concurrent modification
        :param other: Iterable-like to add to
        :param func: func(element1, element2) -> new_element
        :return: self
        """
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
        """
        Inverse of I.add(), combines with another Iterable-like with function 'func'
        If no function is given will default to removing the 'other's elements from self
        :param other: Iterable-like to subtrace from
        :param func_inv: func(element1, element2) -> new_element
        :return: self
        """
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
        """
        Chop the Iterable into other Iterables using a binning function 'func'
        Each keypair is assigned a value -infinity to +infinity, and put into other iterables
        with the same number. These 'bins' are then ordered relatively to each other and returned in a list
        :param func: func(k, v) -> int
        :return: List of Iterables
        """
        chopped = []
        data = {}
        for el in self._elements:
            idx = func(el.id, el.value)
            if not isinstance(idx, int):
                raise ValueError("Chop function returned non-integer value")
            if idx in data:
                data[idx][el.id] = el.value
            else:
                data[idx] = self.__class__({el.id: el.value})
        for k, v in data.items():
            chopped.insert(k, v)

        return chopped

    def funcmap(self, other, comb, mapp, inplace=True):
        """
        Combine self and Iterable-like 'other' with function 'comb'
        Using mapping 'mapp' Can be in-place or not.

        :param other: Iterable-like to combine with
        :param comb: combine function with signature comb(value1, value2) -> new_value
        :param mapp: mapping function with signature mapp(self_key) -> other_key
        :param inplace: Boolean to change self, or return a modified copy
        :return: Iterable
        """
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
            fval = comb(val1, val2)
            d._elements[idx].value = fval

        return d

    def fold_left(self, func):
        """
        Reduce the Iterable using function 'func' and the 'left' grouping pattern
        Like (((1 + 2) + 3) + 4) so
        func(func(func(element1, element2), element3), element4)
        :param func: func(element1, element2) -> new_element
        :return: Element
        """
        if len(self._elements) < 2:
            return self  # Can't fold unless we have at least 2 elements

        tmp_el = self._elements[0]
        for el in self._elements[1:]:
            result = func(tmp_el, el)
            tmp_el = self._eltype(result)
        return tmp_el

    def fold_right(self, func):
        """
        Reduce the Iterable using function 'func' and the 'right' grouping pattern
        Like (1 + (2 + (3 + 4))) so
        func(element1, func(element2, func(element3, element4)))
        :param func: func(element1, element2) -> new_element
        :return: Element
        """
        if len(self._elements) < 2:
            return self  # Can't fold unless we have at least 2 elements

        tmp_el = self._elements[-1]
        for idx in range(len(self._elements) - 1, 0, -1):
            result = func(tmp_el, self._elements[idx - 1])
            tmp_el = self._eltype(result)
        return tmp_el

    def multiply(self, other, func=None):
        """
        Multiply self with Iterable-like 'other' using function 'func'
        If func is None, will default to func(element1, element2) -> ((key1, key2), (value1, value2))
        Every element of self is applied to every element of 'other'
        :param other: Iterable-like to multiply by
        :param func: func(element1, element2) -> new_element
        :return: self
        """
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
        """
        Divide self with Iterable-like 'other' using function 'func'
        If func_inv is None, will default to func_inv(element1, element2) -> (key1, value1) or (key2, value2)
        Every element of self is applied to every element of 'other'
        :param other: Iterable-like to multiply by
        :param func_inv: func_inv(element1, element2) -> new_element
        :return: self
        """
        if not isinstance(other, Iterable):
            other = self.__class__(other)
        if not func_inv:
            def func_inv(e1, e2):
                if e1.id[0] == e2.id:
                    return e1.id[1], e1.value[1]
                else:
                    return e1.id[0], e1.value[0]
        return self.multiply(other, func_inv)

    def compare(self, other, comp, agg, mapp=None, inplace=False):
        """
        Compare self with other using comparison func 'comp' aggregate function 'agg' and mapping function 'mapp'
        If no mapping function is given, the default mapping function maps each element at index i in self to an element
        at index i in other. This can cause problems if other and self don't have the same length

        :param other: Iterable-like to compare against
        :param comp: comp(element1, element2) -> new_value
        :param agg: agg([element1, element2, ..]) -> new_value
        :param mapp: mapp(self_key) -> other_key
        :param inplace: Boolean to modify self or use a copy
        :return: Result from the aggregate function
        """
        if not mapp:
            def mapp(x):
                return other.atindex(self.indexof(x)).id

        result = self.funcmap(
            other=other,
            comb=comp,
            mapp=mapp,
            inplace=inplace
        )
        return agg(result)

    def __le__(self, other):
        """
        Compare each element in self to other with <= operator,
        then aggregate the values of each resulting key with AND
        :param other: Iterable-like to compare against
        :return: True if self <= other else False
        """
        agg = self.getfunc("fold_left", DFuncs.AND)
        return self.compare(other, DFuncs.LE, agg).value

    def __lt__(self, other):
        """
        Compare each element in self to other with < operator,
        then aggregate the values of each resulting key with AND
        :param other: Iterable-like to compare against
        :return: True if self < other else False
        """
        agg = self.getfunc("fold_left", DFuncs.AND)
        return self.compare(other, DFuncs.LT, agg).value

    def __ge__(self, other):
        """
        Compare each element in self to other with >= operator,
        then aggregate the values of each resulting key with AND
        :param other: Iterable-like to compare against
        :return: True if self >= other else False
        """
        agg = self.getfunc("fold_left", DFuncs.AND)
        return self.compare(other, DFuncs.GE, agg).value

    def __gt__(self, other):
        """
        Compare each element in self to other with > operator,
        then aggregate the values of each resulting key with AND
        :param other: Iterable-like to compare against
        :return: True if self > other else False
        """
        agg = self.getfunc("fold_left", DFuncs.AND)
        return self.compare(other, DFuncs.GT, agg).value

    ##
    # @staticmethod  # known case of __new__
    # def __new__(*args, **kwargs):  # real signature unknown
    #     """ Create and return a new object.  See help(type) for accurate signature. """
    #     raise NotImplementedError

    # def __delitem__(self, *args, **kwargs):  # real signature unknown
    #     """ Delete self[key]. """
    #     raise NotImplementedError
    #

    def __eq__(self, other):
        """
        Check if this Iterable is equal to another Iterable-like 'other'
        Must have the same length, and each key must have the same value, order doesn't matter
        :param other: Iterable-like to compare equality
        :return: Boolean
        """
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
        """
        Default behavior the same as self.update(other)
        Returns new instance, doesn't modify self
        :param other: Iterable-like to add
        :return: Added Iterables
        """
        return self.copy().add(other, func=None)

    def __sub__(self, other):
        """
        Default behavior the same as self.unupdate(other)
        Returns new instance, doesn't modify self
        :param other: Iterable-like to sub
        :return: Difference of Iterables
        """
        return self.copy().sub(other, func_inv=None)

    def __mul__(self, other):
        """
        Multiply self by other
        Returns new instance, doesn't modify self
        :param other: Iterable-like
        :return: Multiplied Iterable
        """
        return self.copy().multiply(other, func=None)

    def __truediv__(self, other):
        """
        Divide self by other, inverse of multiplication
        Returns new instance, doesn't modify self
        :param other: Iterable-like
        :return: Divided Iterable
        """
        return self.copy().divide(other, func_inv=None)

    def __iter__(self):
        """
        Get an iterable instance from I, similar to iter(dict) iterates on the keys
        :return: iter of the keys
        """
        return iter(self.keys())

    def __contains__(self, item):
        """
        Check whether item exists in self, where item is a key in the Iterable
        :param item: Key to check if it exists
        :return: True if item in self else False
        """
        return self._indexes.has(item)

    def __getitem__(self, k):
        """
        Get an item from I
        x.__getitem__(y) <==> x[y]
        :param k: Key to retrieve
        :return: Value at key 'k'
        """
        return self.get(k)

    def __setitem__(self, key, value):
        """
        Set self[key] to value. If key doesn't exist, create it
        :param key: key to set
        :param value: value to set under key
        :return: None
        """
        if self._indexes.has(key):
            self._elements[self._indexes.get(key)].value = value
        else:
            self.insert(len(self), (key, value))

    def __len__(self):
        """
        Get the number of elements in self
        :return: Integer length of elements in self
        """
        return len(self._elements)

    def __repr__(self):
        """
        Get the string-like representation of this object, fit for eval()
        :return: Constructor to create this instance with the same data
        """
        return "{cls}({data})".format(
            cls=str(self.__class__.__name__),
            data=str(self)
        )

    def __str__(self):
        """
        Get the string representation of this object, should be the same as str(dict)
        :return: String representing this Iterable
        """
        return str(self.todict())


class OrderedIterableMixin(Iterable):
    """
    Mixin of Iterable, specializing in keeping the order of the elements intact
    through any internal operations.
    """
    def insert(self, index, obj):
        """
        Insert an object into the OrderedIterable, raises a KeyError if the key already exists
        Index value is used to place the object, and then we must update our indexes dict
        :param index: Value to insert element to
        :param obj: Object to insert into the Iterable. Must conform with the element type of the iterable
        :return: Element that was inserted
        """
        element = self._eltype(obj)
        if self._indexes.has(element.id):
            raise KeyError("Key '{}' already exists!".format(element.id))

        self._elements.insert(index, element)
        self._update_indexes(index)
        return element

    def pop(self, k, v_alt=None):
        """
        I.pop(k[,v_alt]) -> v, remove specified key and return the corresponding value.
        If key is not found, v_alt is returned if given, otherwise KeyError is raised.
        After the pop an indexes update must be performed
        :param k: key to pop
        :param v_alt: alternate value if k doesn't exist
        :return: The retrieved value from key k
        """
        if self._indexes.has(k):
            idx = self._indexes.get(k)
            result = self._elements.pop(idx).value
            self._update_indexes(idx)
            return result
        elif v_alt:
            return v_alt
        raise KeyError("Key '{}' not found!".format(k))

    @staticmethod
    def fromkeys(sequence, value=None):
        """
        Create an OrderedIterable instance using a list, each element will be used as a key,
        with each with value 'value'
        :param sequence: List of keys to use
        :param value: Value to set for each key
        :return: Instance with keys from 'sequence' with value 'value'
        """
        raise NotImplementedError("Can't call .fromkeys() on OrderedIterator!")


class Element(object):
    """
    Element superclass of an item in an Iterable
    Must have an id and value, where id is unique to the Element
    Subclasses can give other restrictions to what can and can't be used
    """
    def __init__(self, _id=None, value=None):
        """
        Create a new Element, must include either id and value or just id
        If just id is used, it will attempt to parse it into self.id and self.value
        Otherwise, self.id = id and self.value = value
        :param _id: Id of Element, or object to be parsed
        :param value: Value of the element, required if _id isn't going to be parsed
        """
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
        """
        Parse an object into an Element type, possibly raising InvalidElementTypeException if the object cannot be
        parsed
        :param obj: Element-like object to be parsed
        :return: Element
        """
        raise NotImplementedError("Can't parse object as an Element!")

    def parts(self):
        """
        Break down the Element into a tuple, with (id, value)
        :return: (id, value)
        """
        return self.id, self.value

    def __eq__(self, other):
        """
        Check if self == other
        Not implemented for Element
        :param other: Element-like
        :return: True or False
        """
        raise NotImplementedError("Can't equate superclass Element!")

    def __str__(self):
        """
        String representation of the Element
        :return: String representing self
        """
        return "<{}, {}>".format(self.id, self.value)

    def copy(self):
        """
        Make a shallow copy of self
        :return: Copied version of self
        """
        return self.__class__(self.id, self.value)


class KeyValuePair(Element):
    """
    Basic Element implementation
    """
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
        """
        Check if self == other
        if other is a KeyValuePair, other.id == self.id and self.value == other.value
        if other is a tuple, treat it as (id, value) and check for equality there
        :param other: Element-like
        :return: True or False
        """
        if isinstance(other, dict) and len(other) == 1:
            k, v = list(other.items())[0]
            if k == self.id and v == self.value:
                return True
        elif isinstance(other, KeyValuePair) and other.id == self.id and self.value == other.value:
            return True
        elif isinstance(other, tuple) and self.id == other[0] and self.value == other[1]:
            return True
