Notable and  Useful Functions
*****************************
The dict-plus library contains a multitude of interesting and
useful functions. Here is some documentation on what they are and examples.

- Squish_
- Expand_
- Map_
- ReKey_
- Swap_
- Add_
- Sub_


.. _squish:

Squish
======
Combine two keys and their values into one new key, using a given function. Inverse of Expand_

.. figure:: images/squish.png

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

.. figure:: images/expand.png

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

.. figure:: images/map.png

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

.. figure:: images/rekey.png

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

.. figure:: images/swap.png



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
If no function is given, it's behavior is similar to ``update``

.. figure:: images/add.png

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



.. _sub:

Sub
===
Subtract two dictionaries with a function. Inverse of Add_

To ensure the dictionaries subtract the way you want it to, use an ``OrderedDictPlus``
If no function is given, it's behavior is similar to ``unupdate``

.. figure:: images/sub.png

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



