TODO
----
- All Types
 + `__reversed__`
 +` __hash__`
 + `__format__`
 + `__del__ ? and __delitem__`
 + `__missing__`
 + `__isub__, __iadd__ etc..`
 + `__rsub__, __radd__ etc..`
 + Slicing
 + make into metaclass?

- DictPlus
    + Enhance Pytest
    + set agg func, map func, sub func other than defaults?
    + Subclasses!
        - FunctionDictPlus
        - FunctionallyOrderedDictPlus
        - TwoWayDictPlus
        - HookedDictPlus
        - OneWayDictPlus ? (hashing?)
        - SerializableDictPlus (mixin?)
        - ImmutableDictPlus 
        - UniqueDictPlus (???)

- ListPlus
    + Enhance Pytest
    + Two SuperTypes of List
        - Homogeneous
        - NonHomogeneous
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
    + Enhance Pytest
    + Add internal schema to check if pure or mixed
    + Ops
        - Add/Sub/Multiply/Divide/Etc from super ListPlus?
    + Two SuperTypes of ListDict
        - PureListDict (All keys in subdicts must be well defined, same type etc)
        - MixedListDict (Subdict keys can be missing and have different types)


- README
    + Update documentation
    + add examples for each type of dict/list/etc

- Bugs
    + Recursive .todict() currently fails I believe
    + See 'Issues'

- Utilities
    + Helper func to run Dict, List and ListDict ops easily, just helper_func(python_dict, "func name", func_params)?
        - check out Iterable.getfunc

- Misc
    + Python typings?
    + Add Schema req to dict/list/etc
    + runtime language to describe transforms?
        - DTL (dict transform language?)/JTL (json transform language?)
        - get_dtl (from ops used on dict from creation)
        - clear_dtl (clear ops and start from new on existing dict)
