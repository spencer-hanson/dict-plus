set agg func, map func, sub func other than defaults?

__reversed__
__hash__
__format__
__del__ ? and __delitem__
__missing__
__isub__, __iadd__ etc..
__rsub__, __radd__ etc..
Slicing
make into metaclass?

Subclasses!

    - FunctionDictPlus
    - FunctionallyOrderedDictPlus
    - TwoWayDictPlus
    - HookedDictPlus
    - OneWayDictPlus
    - SerializableDictPlus
    - ImmutableDictPlus
    - UniqueDictPlus


TODO
----
- ListPlus
    + Two SuperTypes of List
    + Homogeneous
        -
    + NonHomogeneous
        -
    + Both
        - Fold L, R
        - Map
        - Chop
        - Squish
        - Expand
        - Scramble?(Rekey)
        - Add/Sub/Multiply/Divide
        - FuncMap
        - Compare (LT, GT, LTE, GTE, EQ, NEQ)

-  ListDict
    + Two types of operations
    + ForEachMapping Op ListDict -> ListDict
        - Map (Each subdict)
        - SubMap (each key of each subdict)
        - PopEach (pop off a key in each subdict)
        - InsertEach (insert a key to each subdict, with context on which subdict)
        - PopMap (pop keys off in each dict, mapping to a new key in each dict)
    + ForEachTransform Op ListDict -> Dict
        - Pop Transform (pop keys off in each dict, mapping to a new dict)
        - Aggregate (take each key of each inner dict and move it to a dict with list keys of the same type)
    + Ops
        - Hoist (take a key from each subdict and return a list of them)
        - Hoist multiple
        - Pop by Regex
        - Add/Sub/Multiply/Divide/Etc from super ListPlus
        -

    + Two SuperTypes of ListDict
        - PureListDict (All keys in subdicts must be well defined, same type etc)
        - MixedListDict (Subdict keys can be missing and have different types)

- DictPlus
    + Disaggregate (take each key and attempt to undo the aggregate func from listdictplus, can fail)
    + Remove Prefix (wont fail unless there's a collision)
    + Pop By Regex

- README
    + Update documentation
    + add examples for each type of dict/list/etc

- Bugs
    + Recursive .todict() currently fails I believe
    + See 'Issues'

- Utilities
    + Helper func to run Dict, List and ListDict ops easily, just helper_func(python_dict, "func name", func_params)?
    +

- Misc
    + (DONE) Reorganize package into a dicts/ folder
    + Python typings
    + Add Schema req to dict/list/etc
    + runtime language to describe transforms?
        - DTL (dict transform language?)
        - JTL (json transform language?)
        - get_dtl (from ops used on dict from creation)
        - clear_dtl (clear ops and start from new on existing dict)