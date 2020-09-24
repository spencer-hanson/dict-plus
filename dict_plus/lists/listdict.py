from dict_plus.dicts import DictPlus
from dict_plus.exceptions import InvalidSubDictType


class ListDict(object):
    def __init__(self, data=None, subdict_type=None):
        if subdict_type is None:
            subdict_type = DictPlus
        if not isinstance(subdict_type, type(DictPlus)):
            raise InvalidSubDictType("Invalid subdict type '{}' Must be subclassed under DictPlus".format(type(subdict_type)))

        self._subdict_type = subdict_type
        self._data = []  # TODO replace this with a ListPlus
        if data is not None:
            for d in data:
                self._data.append(subdict_type(d))

    def map(self, mapfunc):
        # TODO Map (Each subdict)
        return self

    def submap(self, mapfunc):
        # TODO SubMap (each key of each subdict)
        return self

    def inserteach(self, key, value, overwrite_exist=False):
        # TODO InsertEach (insert a key to each subdict, with context on which subdict)
        # if overwrite_exist is True will replace the value
        # if it's false, will ignore
        return self

    def popeach(self, key_name, nonexist_value=None):
        # TODO PopEach (pop off a key in each subdict)
        # if the key doesn't exist, will return the nonexist value in the list
        return []

    def popmap(self, key, mapfunc):
        # TODO PopMap (pop keys off in each dict, mapping to a new key in each dict)
        return self

    def poptransform(self, key, mapfunc=None):
        # TODO Pop Transform (pop keys off in each dict, mapping to a new dict)
        # default behavoir is to keep data the same after popping it off
        return {}

    def popregex(self, regex, use_nonexist=False, nonexist_value=None):
        # TODO pop each key in each subdict matching the regex, returning a dict of lists
        # if use_nonexist==True, go through the entire listdict to get all matching regexes,
        # before checking all dicts for all keys, then inserting nonexist_value in those places
        # else just match per subdict
        return {}

    def aggregate(self, placeholder=None, use_placeholder=True):
        # TODO Aggregate (take each key of each inner dict and move it to a dict with list keys of the same type)
        # If use_placeholder, will insert placeholder inbetween dicts that don't have common keys
        return {}

    def hoist(self, key, nonexist_value=None):
        # TODO Hoist (take a key from each subdict and return a list of them)
        # if key doesn't exist return nonexist value in the place
        return []

    def hoist_multiple(self, keylist, nonexist_value=None):
        # TODO hoist per key and return a dict with keys of keylist, and
        # values of lists of the values
        return {}
