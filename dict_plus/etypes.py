"""
Python version compatible type import helper
Exported types:
- DictType
- ListType
- StringTypes
"""

import six


if six.PY2:
    from types import DictType, ListType, StringTypes
else:
    DictType = dict
    ListType = list
    StringTypes = str


class _NoneVal(object):
    """ None Value object, used to differentiate between python's None and *actually* nothing"""
    pass


NoneVal = _NoneVal()

