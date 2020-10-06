from dict_plus.dicts import DictPlus
from dict_plus.lists.listplus import ListPlus
from dict_plus.exceptions import InvalidSubDictType
from dict_plus.etypes import NoneVal
import re


class ListDict(ListPlus):
    def __init__(self, data=None, subdict_type=None):
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
        # Map (Each subdict)
        data = []
        for d in self:
            data.append(mapfunc(d))
        return self

    def submap(self, mapfunc):
        # SubMap (each key of each subdict)
        for d in self:
            d.map(mapfunc)
        return self

    def inserteach(self, key, value, overwrite_exist=False):
        # InsertEach (insert a key to each subdict, with context on which subdict)
        # if overwrite_exist is True will replace the value
        # if it's false, will ignore
        for d in self:
            if key in d:
                if overwrite_exist:
                    d[key] = value
            else:
                d[key] = value

        return self

    def popeach(self, key_name, nonexist_value=NoneVal):
        # PopEach (pop off a key in each subdict)
        # if the key doesn't exist, will return the nonexist value in the list
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
        # PopMap (pop keys off in each subdict, mapping to a new key in each dict)
        # Will overrite key if existing
        for d in self:
            v = d.pop(key, nonexist_value)
            k, v = func(v)
            d[k] = v
        return self
    # Wtf is this supposed to do? Remove maybe? dont remember lol
    # def poptransform(self, key, func=None, nonexist_value=NoneVal):
    #     # Pop Transform (pop keys off in each dict, mapping to a new dict)
    #     # default behavior is to keep data the same after popping it off
    #     if func is None:
    #         func = lambda x: (key, x)
    #     new_d = {}
    #
    #     for d in self:
    #         v = d.get(key, nonexist_value)
    #         k, v = func(v)
    #         new_d[k] = v
    #     return new_d

    def popregex(self, regex, nonexist_value=None):
        # Pop each key in each subdict matching the regex, returning a list of dicts
        # if use_nonexist==True, go through the entire listdict to get all matching regexes,
        # before checking all dicts for all keys, then inserting nonexist_value in those places
        # else just match per subdict
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
        # Aggregate (take each key of each inner dict and move it to a dict with list keys of the same type)
        # If use_placeholder, will insert placeholder inbetween dicts that don't have common keys
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
        # Hoist (take a key from each subdict and return a list of them)
        # if key doesn't exist return nonexist value in the place
        vals = []
        for d in self:
            if key in d:
                vals.append(d[key])
            else:
                vals.append(nonexist_value)
        return vals

    def hoist_multiple(self, keylist, nonexist_value=None):
        # Hoist per key and return a dict with keys of keylist, and
        # values of lists of the values
        new_d = self._subdict_type()
        for k in keylist:
            new_d[k] = self.hoist(k, nonexist_value)

        return new_d

    def indexof(self, key):
        raise NotImplementedError
