from dict_plus.dicts import DictPlus
from dict_plus.lists.listplus import ListPlus
from dict_plus.exceptions import InvalidSubDictType
from dict_plus.etypes import NoneVal
import re


class ListDict(ListPlus):
    """
    List of Dictionaries container
    """
    def __init__(self, data=None, subdict_type=None):
        """
        Create a new list of dictionaries
        Args:
            data: iterable list of dictionaries
            subdict_type: DictPlus classtype for the subdicts to be typed
        """
        super(ListDict, self).__init__()

        if subdict_type is None:
            subdict_type = DictPlus
        if not isinstance(subdict_type, type(DictPlus)):
            raise InvalidSubDictType("Invalid subdict type '{}' Must be subclassed under DictPlus".format(type(subdict_type)))

        self._subdict_type = subdict_type

        if data is not None:
            for d in data:
                self.append(subdict_type(d))

    def map(self, mapfunc):
        """
        For each dictionary in the list, map(mapfunc, list of dicts) -> new list of dicts
        Args:
            mapfunc: Function with signature f(d) -> d'

        Returns:
            self
        """

        data = []
        for d in self:
            data.append(mapfunc(d))
        return self

    def submap(self, mapfunc):
        """
        Map each key in each subdictionary to a new value
        Args:
            mapfunc: Function with signature f(k, v) -> k', v'
        Returns:
            self
        """

        for d in self:
            d.map(mapfunc)
        return self

    def inserteach(self, key, value, overwrite_exist=False):
        """
        InsertEach (insert a key to each subdict, with context on which subdict)
        if overwrite_exist is True will replace the value if it exists
        if it's false, will ignore the value if it exists

        Args:
            key: Key to insert
            value: value to insert
            overwrite_exist: Overwrite existing key/values

        Returns:
            self
        """
        #
        for d in self:
            if key in d:
                if overwrite_exist:
                    d[key] = value
            else:
                d[key] = value

        return self

    def popeach(self, key_name, nonexist_value=NoneVal):
        """
        PopEach - pop off a key in each subdict
        if the key doesn't exist, will return nonexist_value if it is set

        Args:
            key_name: key to pop in each subdict
            nonexist_value: Value to replace if they key doesn't exist

        Returns:
            list of vals
        """

        vals = []
        for d in self:
            if key_name in d:
                vals.append(d.pop(key_name))
            elif nonexist_value is not NoneVal:
                vals.append(nonexist_value)
            else:
                raise KeyError("Key '{}' not found in all subdicts!".format(key_name))
        return vals

    def popmap(self, key, func, nonexist_value=NoneVal):
        """
        PopMap - pop keys off in each subdict, mapping to a new key, in each subdict
        Will overwrite key if key exists
        Args:
            key: Key to pop in each subdict
            func: Function with signature f(v) -> k', v'
            nonexist_value: If key doesn't exist, use this value instead

        Returns:
            self
        """

        for d in self:
            v = d.pop(key, nonexist_value)
            k, v = func(v)
            d[k] = v
        return self

    def popregex(self, regex, nonexist_value=None):
        """
        Pop each key in each subdict matching the regex, returning a list of dicts
        if use_nonexist==True, go through the entire listdict to get all matching regexes,
        before checking all dicts for all keys, then inserting nonexist_value in those places
        else just match per subdict
        Args:
            regex: regex to match against
            nonexist_value: value to insert if the key doesn't exist in one of the subdicts

        Returns:
            new ListDict() from popped data
        """

        data = []

        if not nonexist_value:
            for d in self:
                subdata = {}
                for k, v in d.items():
                    if re.match(regex, k):
                        subdata[k] = d.pop(k)
                data.append(subdata)
        else:
            matched_keys = []
            for d in self:
                for k, v in d.items():
                    if re.match(regex, k):
                        matched_keys.append(k)
            matched_keys = list(set(matched_keys))
            for d in self:
                subdata = {}
                for k in matched_keys:
                    if k in d:
                        subdata[k] = d.pop(k)
                    else:
                        subdata[k] = nonexist_value
                data.append(subdata)

        return self.__class__(data)

    def aggregate(self, placeholder=NoneVal):
        """
        Aggregate (take each key of each inner dict and move it to a dict with list keys of the same type)
        If use_placeholder, will insert placeholder inbetween dicts that don't have common keys.

        Use DictPlus.disaggregate(placeholder) to undo this operation
        Args:
            placeholder: value to insert if a key doesn't exist within a subdict
        Returns:
            aggregated dict
        """

        new_d = self._subdict_type()
        if placeholder is NoneVal:
            for d in self:
                for k, v in d.items():
                    if k in new_d:
                        new_d[k].append(v)
                    else:
                        new_d[k] = [v]
        else:
            all_keys = []  # TODO move this to an internal index
            for d in self:
                all_keys.extend(d.keys())
            all_keys = list(set(all_keys))
            for d in self:
                for k in all_keys:
                    if k in d:
                        val = d[k]
                    else:
                        val = placeholder

                    if k in new_d:
                        new_d[k].append(val)
                    else:
                        new_d[k] = [val]
        return new_d

    def hoist(self, key, nonexist_value=None):
        """
        Hoist - take a key from each subdict, and pop it off, returning a list of values
        Args:
            key: key to pop from each subdict
            nonexist_value: if the key doesn't exist in the subdict, use this value instead

        Returns:
            list of values
        """

        vals = []
        for d in self:
            if key in d:
                vals.append(d[key])
            else:
                vals.append(nonexist_value)
        return vals

    def hoist_multiple(self, keylist, nonexist_value=None):
        """
        Hoist multiple keys from each subdict, into a dictionary with keys 'keylist' where the values are lists
        of values within each subdict
        Args:
            keylist: list of keys within the subdicts
            nonexist_value: value to insert when the the key doesn't exist

        Returns:
         dict of lists
        """
        new_d = self._subdict_type()
        for k in keylist:
            new_d[k] = self.hoist(k, nonexist_value)

        return new_d
