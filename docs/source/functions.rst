Notable Functions
*****************
The dict-plus library contains a multitude of interesting and
useful functions. Here is some documentation on what they are and examples.

- Squish_
- Expand_
- Map_
- ReKey_
- Swap_
- Add_
- Sub_
- Multiply_
- Chop_
- Divide_
- FuncMap_
- FoldLeft_
- FoldRight_
- Compare_
- LessThan_
- GreaterThan_
- GreaterThanEqual_
- LessThanEqual_
- Equal_
- NotEqual_


.. _squish:

Squish
======
Combine two keys and their values into one new key, using a given function. Inverse of Expand_


The function signature looks as follows:

``func(value_list) -> new_value``

This example squishes the keys '1' and 'asdf'  into a key called  'tt', with a function
that takes the values, '8'  and '[E]' respectively, and combines them.

.. code:: python

    d = DictPlus({"1": "8", "asdf": "[E]"})
    d.squish(["1", "asdf"], "tt", lambda x: x[0] + x[1])
    assert_eq(d, {"tt": "8[E]"})


.. _expand:

Expand
======
Expand a single key into any number of keys. Inverse of Squish_



The function signature looks as follows:

``func(value) -> value_list``

This example expands the key 'tt'  into keys '1' and 'asdf', with a function that takes the value of 'tt'
and splits it into two strings. The output length must match the number of keys.

.. code:: python

    d = DictPlus({"tt": "8[E]"})
    d.expand("tt", ["1", "asdf"], lambda x: (x[0], x[1:]))
    assert_eq(d, {"1": "8", "asdf": "[E]"})



.. _map:

Map
===
Map a dictionary to new keys and values.


The function signature looks as follows:

``func(key, value) -> new_key, new_value``


In this example, a simple dictionary is mapped with a function that doubles it's value and appends 'a'
to it's key. It is then un-done with an inverse function.

.. code:: python

    # Function element to element
    def func_e2e(k, v):
        return str(k) + "a", v * 2

    def invfunc_e2e(k, v):
        return str(k)[:-1], v / 2

    d = DictPlus({"a": 1, "b": 2, "c": 3})

    d.map(func_e2e)
    assert_eq(d, {"aa": 2, "ba": 4, "ca": 6})

    d.map(invfunc_e2e)
    assert_eq(d, {"b": 2, "c": 3})


.. _rekey:

ReKey
=====
Change the keys of a dictionary, keeping the values the same. Converse of Swap_



The function signature looks as follows:

``func(key) -> new_key``


In this example, the keys in a dictionary are prepended with 'a', and  then removed with an inverse function.

.. code:: python

    # Function key to key
    def func_k2k(k):
        return k + "a"

    def invfunc_k2k(k):
        return k[:-1]

    d = DictPlus({"a": 1, "b": 2})
    d.rekey(func_k2k)
    assert_eq(d, {"aa": 1, "ba": 2})

    d.rekey(invfunc_k2k)
    assert_eq(d, {"a": 1, "b": 2})


.. _swap:

Swap
====
Swap two keys, keeping the values the same. Converse of ReKey_





In this example, the keys 'a' and 'b' are swapped

.. code:: python

    d = DictPlus({"a": 1, "b": 2})
    d.swap("a", "b")
    assert_eq(d["a"], 2)
    assert_eq(d["b"], 1)



.. _add:

Add
===
Add two dictionaries with a function. Inverse of Sub_

To ensure the dictionaries add the way you want it to, use an ``OrderedDictPlus``
If no function is given, it's behavior is similar to ``update`` and can be used with addition
symbol ``+``



The function signature looks as follows:

``func(key_value_pair1, key_value_pair2) -> new_key_value_pair``


In this example, two dictionaries are added together using a function that adds their keys and values.
Also, they are added without a function, and their keys are added, with common keys overriding, giving
precedence to the right dictionary. Can be added with any dict-like object

.. code:: python

    # Function element,element to element
    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    d = OrderedDictPlus({"a": 1, "b": 2})
    d2 = {"c": 3, "d": 4}

    d3 = d + d2 # d3 equals {"a": 1, "b": 2, "c": 3, "d": 4}
    d.add(d2) # d is now {"a": 1, "b": 2, "c": 3, "d": 4}

    d = OrderedDictPlus({"a": 1, "b": 2}) # reset value of d
    d.add(d2, func_ee2e) # d is now {"ac": 4, "bd": 6}

    # This also works if you use '+'
    # so d + {} -> result would be d
    # When using the symbol, the original dictionary is not changed

.. _sub:

Sub
===
Subtract two dictionaries with a function. Inverse of Add_

To ensure the dictionaries subtract the way you want it to, use an ``OrderedDictPlus``
If no function is given, it's behavior is similar to ``unupdate`` and can be used with subtraction
symbol ``-``



The function signature looks as follows:

``func(key_value_pair1, key_value_pair2) -> new_key_value_pair``


In this example, two dictionaries are subtracted using a function that subtracts their keys and values.
Also, they are subtracted without a function, and their keys are removed. Unshared keys are ignored.
Can be subtracted with any dict-like object

.. code:: python

    # Function element,element to element
    def func_ee2e(e1, e2):
        return e1.id - e2.id, e1.value - e2.value

    d = OrderedDictPlus({"a": 1, "b": 2, "c": 3, "d": 4})
    d2 = {"c": 3, "d": 4}

    d3 = d - d2 # d3 equals {"a": 1, "b": 2}
    d.sub(d2) # d is now {"a": 1, "b": 2}

    d = OrderedDictPlus({"a": 1, "b": 2, "c": 3, "d": 4}) # Reset value of d
    d.sub(d2, func_ee2e) # d is now equals {"ac": 4, "bd": 6}

    # This also works if you use '-'
    # so d - {} -> result would be d
    # When using the symbol, the original dictionary is not changed

.. _chop:

Chop
====

Chops the dictionary into other dictionaries using a binning function
Each keypair is assigned an integer value, and put in with other dictionaries with the same number.
These 'bins' are then ordered relatively to each other and returned as a list.

Function signature looks as follows:

``func(k, v) -> int``



In this example, a dictionary with integer keys and string values is created, and chopped up into
two other dictionaries where one has only even keys and the other only odd keys.


.. code:: python

    d = DictPlus({
        0: "a", 1: "b", 2: "c",
        3: "d", 4: "e", 5: "f",
        6: "g", 7: "h"
    })

    def func_chop(k, v):
        # Chops into even and odd keys
        return int(k % 2 != 0)

    chopped = d.chop(func_chop)
    # chopped[0] is now {0: "a", 2: "c", 4: "e", 6: "g"}
    # chopped[1] is now {1: "b", 3: "d", 5: "f", 7: "h"}


.. _multiply:

Multiply
========
Multiply two dictionaries. Inverse of Divide_

Multiply ``self`` with Iterable-like ``other`` using a function, such that every element
of ``self`` is applied to every element of ``other``

Function signature looks as follows:

``func(element1, element2) -> (newkey1, newvalue1)``

If the passed func is None, it defaults to:

``func(element1, element2) -> ((key1, key2), (value1, value2))``
and can be used with the multiplication symbol ``*``

In the example below, a simple dictionary is multiplied in different ways with different functions
and the results are shown in the comments




.. code:: python


    d = OrderedDictPlus({"a": 1, "b": 2, "c": 3})
    d.multiply({})  # Multiplying by an empty dict is like multiplying by zero, so d is now {}
    d = OrderedDictPlus(o)

    d.multiply(o)
    # d is now:
    #{
    #    ("a", "a"): (1, 1), ("a", "b"): (1, 2), ("a", "c"): (1, 3),
    #    ("b", "a"): (2, 1), ("b", "b"): (2, 2), ("b", "c"): (2, 3),
    #    ("c", "a"): (3, 1), ("c", "b"): (3, 2), ("c", "c"): (3, 3)
    #}

    d = OrderedDictPlus({"a": 1, "b": 2, "c": 3})  # Reset d
    d.multiply({"a": 1, "b": 2, "c": 3}, lambda e1, e2: e1)  # Now we multiply using a function that always returns the first operand
    # This is essentially multiplying by 1, we get the original dictionary

    # Now we multiply with a more complex function, adds the keys and makes the values tuples
    d.multiply({"a": 1, "b": 2, "c": 3}, lambda e1, e2: (e1.id + e2.id, (e1.value, e2.value)))
    # d is now:
    #{
    #    "aa": (1, 1), "ab": (1, 2), "ac": (1, 3),
    #    "ba": (2, 1), "bb": (2, 2), "bc": (2, 3),
    #    "ca": (3, 1), "cb": (3, 2), "cc": (3, 3)
    #}

    # This also works if you use '*'
    # so d * {}, result would be {}
    # When using the symbol, the original dictionary is not changed

.. _divide:

Divide
======
Divide two dictionaries. Inverse of Multiply_

Divide ``self`` with Iterable-like ``other`` using a function.

Function signature looks as follows:

``func(element1, element2) -> (newkey1, newvalue1)``

If func_inv is ``None``, it defaults to:

``func_inv(element1, element2) -> (key1, value1) or (key2, value2)``

and can be used with the division symbol ``/``

Every element of ``self`` is applied to every element of ``other`` This is meant to undo what
multiply did, it won't work if you change the order of the dictionary.



In this example, the division is used to undo the result of a multiplication (o1),
to retrieve the original dictionary (o2)

.. code:: python

     o = {
            ("a", "a"): (1, 1), ("a", "b"): (1, 2), ("a", "c"): (1, 3),
            ("b", "a"): (2, 1), ("b", "b"): (2, 2), ("b", "c"): (2, 3),
            ("c", "a"): (3, 1), ("c", "b"): (3, 2), ("c", "c"): (3, 3)
        }
        o2 = {"a": 1, "b": 2, "c": 3}
        d = OrderedDictPlus(o)
        d.divide(o, lambda el, e2: (el.id[0], el.value[0]))
        # d is now o2

    # This also works if you use '/'
    # so d / {}, result would be {}
    # When using the symbol, the original dictionary is not changed

.. _FuncMap:

FuncMap
=======
Combine self and Iterable-like 'other' with a combine function and
using a mapping function. Can be in-place or not.

Combine function signature looks as follows:

``func(value1, value2) -> new_value``

Mapping function signature looks as follows:

``func(key) -> new_key``

The following code combines the values by multiplying, and mapping to the opposite end of the dictionary

.. code:: python

        d = DictPlus({a: a for a in range(0, 100)})
        dp = d.funcmap(
            {a: a for a in range(0, 100)},
            lambda _v1, _v2: _v1 * _v2,
            lambda _id: 99 - _id,
            inplace=False
        )
        # dp is now = {a: a * (99 - a) for a in range(0, 100)}

.. _FoldLeft:

Fold Left
=========
Reduce the Iterable using function 'func' and the 'left' grouping pattern
Like (((1 + 2) + 3) + 4) so
func(func(func(element1, element2), element3), element4)

The function signature looks as following:
``func(element1, element2) -> new_element``

.. code:: python

        d = DictPlus({0: "a", 1: "b", 2: "c"})
        r = d.fold_left(lambda e1, e2: (e1.id+e2.id,e1.value+e2.value))
        # r is now {3: "abc"}


.. _FoldRight:

Fold Right
==========
Reduce the Iterable using function 'func' and the 'right' grouping pattern
Like (1 + (2 + (3 + 4))) so
func(element1, func(element2, func(element3, element4)))

The function signature looks as following:
``func(element1, element2) -> new_element``

.. code:: python

        d = DictPlus({0: "a", 1: "b", 2: "c"})
        r = d.fold_left(lambda e1, e2: (e1.id+e2.id,e1.value+e2.value))
        # r is now {3: "cba"}




.. _Compare:

Compare
=======
Compare self with other using a comparison function, an aggregate function and a mapping function.
If no mapping function is given, the default mapping function maps each element at index i in self to an element
at index i in other.
This can cause problems if other and self don't have the same length

The compare function signature looks as following:
``func(element1, element2) -> new_value``

The aggregate function signature looks as following:
``func([element1, element2, ..]) -> new_value``

The mapping function signature looks as following:
``func(self_key) -> other_key``

The following example combines the dictionary and simplifies it to find the truthy value of all the keys

.. code:: python

        d = DictPlus({False: "a", True: "b", False: "c"})
        t = d.compare({False: "a", True: "b", False: "c"},
                        comp=lambda el1,el2:el1.id,
                        agg=dict_plus.funcs.Functions.AND,
                        mapp=None)
        # t is now false

.. _LessThan:

LessThan
========
Less than is a Compare_ call with the function LT

.. _GreaterThan:

GreaterThan
===========
Greater than is a Compare_ call with the function GT


.. _GreaterThanEqual:

GreaterThanEqual
================
Greater tha equal is a Compare_ call with the function GTE


.. _LessThanEqual:

LessThanEqual
=============
Greater than is a Compare_ call with the function LTE


.. _Equal:

Equal
=====
Equal is a Compare_ call with the function EQ

.. _NotEqual:

Not Equal
=========
Not Equal is a Compare_ call with the function NEQ
