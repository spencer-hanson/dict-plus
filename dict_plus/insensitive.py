from dict_plus import DictPlus, KeyValuePair, ElementFactory


class FunctionallyInsensitiveDictPlus(DictPlus):

    def __init__(self, data=None, element_type=None, compare_func=None, **kwargs):
        """
        Create a new FunctionallyInsensitiveDictPlus

        Pass in a compare function with signature (new_key, old_key) and it will determine if a given key is equal on
        add,delete,modify,update

        :param compare_func: Function with signature (new_key, old_key)
        :param data: data to use initially in the DictPlus. Can be a tuple list or a dict, or an object with .keys()
        :param element_type: Element type to store the data with, defaults to KeyValuePair
        :param kwargs: keyword args to include in the dict
        """
        super(FunctionallyInsensitiveDictPlus, self).__init__(
            data,
            element_type or ElementFactory.element(KeyValuePair, FunctionallyInsensitiveDictPlus),
            **kwargs)
        self.compare_func = compare_func or self.compare_func

    @staticmethod
    def fromkeys(sequence, value=None):
        """
        Create a new FunctionallyInsensitiveDictPlus from a sequence of keys, all with value 'value'
        :param sequence: iterable of keys
        :param value: value to set each key to, defaults to None
        :return: DictPlus with populated data
        """
        d = FunctionallyInsensitiveDictPlus()
        for item in sequence:
            d.insert(-1, (item, value))
        return d

    def compare_func(self, new_key, old_key):
        """
        If you return True, it exists in the dict, and should be overridden.
        If you return False, the key doesn't match, and if no keys match, it will be added as a new entry
        :param new_key: Key trying to be added to dictionary
        :param old_key: Key already in dictionary to check against
        :return: True if new_key is old_key
        """
        return new_key == old_key

    def _find_base_key(self, new_key):
        for k in self.keys():
            if self.compare_func(new_key, k):
                return k
        return None

    def getitem(self, k, v_alt=None):
        """
        Get the full element from key 'k'
        if no key or value is present, Element(k, v_alt) will be returned
        :param k:
        :param v_alt:
        :return: Element with key 'k'
        """
        base_key = self._find_base_key(k)
        if base_key is not None:
            return self._elements[self._indexes.get(base_key)]
        elif v_alt:
            return self.elements_type(k, v_alt)
        else:
            self._find_base_key(k)
            raise KeyError("No key '{}' found!".format(k))

    def pop(self, k, v_alt=None):
        base_key = self._find_base_key(k)
        if base_key:
            idx = self._indexes.get(base_key)
            result = self._elements.pop(idx).value
            self._update_indexes(idx)
            return result
        elif v_alt:
            return v_alt
        raise KeyError("Key '{}' not found!".format(base_key))

    def update(self, e=None, **kwargs):
        if hasattr(e, "keys"):
            for k in e.keys():
                base_key = self._find_base_key(k)
                if self._indexes.has(base_key):
                    self[base_key] = e[k]
                else:
                    self.insert(len(self), (k, e[k]))
        else:
            for k, v in e:
                base_key = self._find_base_key(k)
                self.insert(len(self), (base_key or k, v))
        for k in kwargs:
            base_key = self._find_base_key(k)
            self.insert(len(self), (base_key or k, kwargs[k]))

    def indexof(self, key):
        base_key = self._find_base_key(key)
        return super(FunctionallyInsensitiveDictPlus, self).indexof(base_key or key)

    def setdefault(self, k, v_alt=None):
        base_key = self._find_base_key(k)
        return super(FunctionallyInsensitiveDictPlus, self).setdefault(base_key or k, v_alt)

    def __contains__(self, item):
        """
        Check whether item exists in self, where item is a key in the Iterable
        :param item: Key to check if it exists
        :return: True if item in self else False
        """
        base_key = self._find_base_key(item)
        return self._indexes.has(base_key or item)

    def __setitem__(self, key, value):
        """
        Set self[key] to value. If key doesn't exist, create it
        :param key: key to set
        :param value: value to set under key
        :return: None
        """
        base_key = self._find_base_key(key)
        if self._indexes.has(base_key):
            self._elements[self._indexes.get(base_key)].value = value
        else:
            self.insert(len(self), (key, value))


class CaseInsensitiveDictPlus(FunctionallyInsensitiveDictPlus):
    def __init__(self, data=None, element_type=None, compare_func=None, **kwargs):
        super(CaseInsensitiveDictPlus, self).__init__(
            data,
            element_type or ElementFactory.element(KeyValuePair, CaseInsensitiveDictPlus),
            compare_func,
            **kwargs)

    def compare_func(self, new_key, old_key):
        """
        If you return True, it exists in the dict, and should be overridden.
        If you return False, the key doesn't match, and if no keys match, it will be added as a new entry
        :param new_key: Key trying to be added to dictionary
        :param old_key: Key already in dictionary to check against
        :return: True if new_key is old_key
        """
        if hasattr(new_key, "lower") and hasattr(old_key, "lower"):
            return new_key.lower() == old_key.lower()
        else:
            return new_key == old_key  # Included for non-string keys

    @staticmethod
    def fromkeys(sequence, value=None):
        """
        Create a new FunctionallyInsensitiveDictPlus from a sequence of keys, all with value 'value'
        :param sequence: iterable of keys
        :param value: value to set each key to, defaults to None
        :return: DictPlus with populated data
        """
        d = CaseInsensitiveDictPlus()
        for item in sequence:
            d.insert(-1, (item, value))
        return d


class PrefixInsensitiveDictPlus(FunctionallyInsensitiveDictPlus):
    def __init__(self, data=None, element_type=None, prefix_list=[], **kwargs):
        if not isinstance(prefix_list, list):
            prefix_list = [prefix_list]

        compare_func = self._get_compare_func(prefix_list)

        super(PrefixInsensitiveDictPlus, self).__init__(
            data,
            element_type or ElementFactory.element(KeyValuePair, PrefixInsensitiveDictPlus),
            compare_func=compare_func,
            **kwargs)

    def set_prefix_list(self, new_prefix_list):
        if not isinstance(new_prefix_list, list):
            new_prefix_list = [new_prefix_list]
        self.compare_func = PrefixInsensitiveDictPlus._get_compare_func(new_prefix_list)

    @staticmethod
    def _get_compare_func(prefix_list):
        def compare_func(new_key, old_key):
            """
            If you return True, it exists in the dict, and should be overridden.
            If you return False, the key doesn't match, and if no keys match, it will be added as a new entry
            :param new_key: Key trying to be added to dictionary
            :param old_key: Key already in dictionary to check against
            :return: True if new_key is old_key
            """
            if new_key == old_key:
                return True

            def unprefix_key(key):
                for prefix in prefix_list:
                    if key.startswith(prefix):
                        return key.replace(prefix, "")  # Remove prefix
                return key  # No prefix to remove

            new_key = unprefix_key(new_key)
            old_key = unprefix_key(old_key)

            if new_key == old_key:
                return True
            else:
                return False

        return compare_func

    @staticmethod
    def fromkeys(sequence, value=None):
        """
        Create a new PrefixInsensitiveDictPlus from a sequence of keys, all with value 'value'
        :param sequence: iterable of keys
        :param value: value to set each key to, defaults to None
        :return: DictPlus with populated data
        """
        d = PrefixInsensitiveDictPlus("")
        for item in sequence:
            d.insert(-1, (item, value))
        return d


class SuffixInsensitiveDictPlus(FunctionallyInsensitiveDictPlus):
    def __init__(self, data=None, element_type=None, suffix_list=[], **kwargs):
        if not isinstance(suffix_list, list):
            suffix_list = [suffix_list]
        compare_func = self._get_compare_func(suffix_list)
        super(SuffixInsensitiveDictPlus, self).__init__(
            data,
            element_type or ElementFactory.element(KeyValuePair, SuffixInsensitiveDictPlus),
            compare_func=compare_func,
            **kwargs
        )

    def set_suffix_list(self, new_suffix_list):
        if not isinstance(new_suffix_list, list):
            new_suffix_list = [new_suffix_list]
        self.compare_func = SuffixInsensitiveDictPlus._get_compare_func(new_suffix_list)

    @staticmethod
    def _get_compare_func(suffix_list):
        def compare_func(new_key, old_key):
            """
            If you return True, it exists in the dict, and should be overridden.
            If you return False, the key doesn't match, and if no keys match, it will be added as a new entry
            :param new_key: Key trying to be added to dictionary
            :param old_key: Key already in dictionary to check against
            :return: True if new_key is old_key
            """
            if new_key == old_key:
                return True

            def unsuffix_key(key):
                for suffix in suffix_list:
                    if key.endswith(suffix):
                        return key.replace(suffix, "")  # Remove suffix
                return key  # No suffix to remove

            new_key = unsuffix_key(new_key)
            old_key = unsuffix_key(old_key)

            if new_key == old_key:
                return True
            else:
                return False

        return compare_func

    @staticmethod
    def fromkeys(sequence, value=None):
        """
        Create a new SuffixInsensitiveDictPlus from a sequence of keys, all with value 'value'
        :param sequence: iterable of keys
        :param value: value to set each key to, defaults to None
        :return: DictPlus with populated data
        """
        d = SuffixInsensitiveDictPlus("")
        for item in sequence:
            d.insert(-1, (item, value))
        return d
