import six


if six.PY2:
    from types import DictType, ListType, StringTypes
else:
    DictType = dict
    ListType = list
    StringTypes = str
