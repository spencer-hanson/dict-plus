from dict_plus.dictplus import *
from dict_plus.insensitive import *
from dict_plus import *
from dict_plus.exceptions import *
import operator

assertions = {
    "op": 0,
    "nop": 0,
    "eq": 0,
    "neq": 0,
    "t": 0,
    "f": 0
}


def ex(f, ex_class, *args, **kwargs):
    try:
        f(*args, **kwargs)
    except Exception as _e:
        assert_eq(_e.__class__, ex_class)
    else:
        raise AssertionError("Didn't throw expected '{}'".format(ex_class.__name__))


def assert_op(val1, val2, op):
    assert op(val1, val2)
    assertions["op"] = assertions["op"] + 1


def assert_nop(val1, val2, op):
    assert not op(val1, val2)
    assertions["nop"] = assertions["nop"] + 1


def assert_eq(val1, val2):
    assert val1 == val2
    assertions["eq"] = assertions["eq"] + 1


def assert_neq(val1, val2):
    assert val1 != val2
    assertions["neq"] = assertions["neq"] + 1


def assert_t(val):
    assert val
    assertions["t"] = assertions["t"] + 1


def assert_f(val):
    assert not val
    assertions["f"] = assertions["f"] + 1


##################


def test_iterableindex():
    class A(object):
        pass

    class B(object):
        __hash__ = None

    ii = Iterable.IterableIndex()

    things_to_hash = [
        [1, 2, 3, 4],
        [1, 2, 3, "4"],
        [[1, 2, 3, "4"], [1, 2, 3, 4]],
        [[A(), 1, "4"], {"a": A(), "b": B()}],
        {"a": A(), "b": [B(), B(), 2]},
        "1",
        {"A", "B", "C"},
        50,
        False,
        -25,
    ]

    for idx, thing in enumerate(things_to_hash):
        ii.set(thing, idx)
        ii.get(thing)


##################


def test_keyvaluepair_parse_object():
    def subtest_keyvaluepair_parse_object(_id, val):
        parse = KeyValuePair.parse_object

        ex(parse, InvalidElementTypeException, (_id, _id, _id))
        ex(parse, InvalidElementTypeException, (val, val, val))

        assert_eq(parse((_id, val)), (_id, val))
        assert_eq(parse((val, _id)), (val, _id))

        assert_eq(parse(KeyValuePair(_id, val)), (_id, val))
        assert_eq(parse(KeyValuePair(val, _id)), (val, _id))

    subtest_keyvaluepair_parse_object("a", "b")
    subtest_keyvaluepair_parse_object("a", 1)
    subtest_keyvaluepair_parse_object(1, 1)


def test_keyvaluepair___eq__():
    assert_eq(KeyValuePair("a", "b"), {"a": "b"})
    assert_eq(KeyValuePair("a", "b"), ("a", "b"))
    assert_neq(KeyValuePair("a", "b"), ("b", "a"))
    kvp = KeyValuePair("a", "b")
    assert_eq(kvp, kvp.copy())


##################


def test_element___init__():
    ex(KeyValuePair, InvalidElementTypeException, "id", None)
    ex(KeyValuePair, TypeError, None, "value")
    assert_eq(KeyValuePair(0, 1), KeyValuePair((0, 1)))
    assert_eq(KeyValuePair(KeyValuePair(0, 1)), KeyValuePair((0, 1)))


def test_element_parts():
    assert_eq(Element(0, 1).parts(), (0, 1))


def test_element___eq__():
    d = OrderedDictPlus()
    d.insert(0, ("4", "3"))
    assert_eq(d.getitem("4"), KeyValuePair("4", "3"))
    assert_eq(("4", "3"), KeyValuePair("4", "3"))
    assert_eq(KeyValuePair("a", "b"), KeyValuePair("a", "b"))
    assert_eq(KeyValuePair("1", "2"), ("1", "2"))
    assert_neq(KeyValuePair("1", "2"), ["1", "2"])
    assert_eq(KeyValuePair("a", "b"), {"a": "b"})
    assert_neq(KeyValuePair("c", "d"), {"a": "b", "c": "d"})


##################

def test_iterable_get():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    assert_eq(d.get("1"), "2")


def test_iterable_getitem():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    assert_neq(d.getitem("1"), 8)
    assert_eq(d.getitem("1"), KeyValuePair("1", "2"))


def test_iterable_insert():
    d = DictPlus()
    assert_t(d.insert(12345, ("a", "g")))
    ex(d.insert, KeyError, 12345, ("a", "b"))
    assert_eq(d._indexes.get("a"), 0)
    assert_eq(d._elements[0], ("a", "g"))


def test_iterable_pop():
    d = DictPlus({"a": "b", "c": "d"})
    assert_eq(d.pop("a"), "b")
    assert_eq(d, {"c": "d"})
    d.insert(1, ("a", "b"))
    assert_eq(d.pop("a"), "b")
    assert_eq(d.pop("c"), "d")
    ex(d.pop, KeyError, "a")


def test_iterable_popitem():
    d = DictPlus({"a": "b"})
    t = d.popitem()
    assert_eq(t, ("a", "b"))
    ex(d.popitem, KeyError)


def test_iterable_copy():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    c = d.copy()
    assert_eq(d, c)

    d.insert(-1, ("[E]", "no u"))
    assert_neq(d, c)
    d.pop("[E]")
    d["1"] = "1"
    assert_neq(d, c)


def test_iterable_atindex():
    d = DictPlus({"a": 1, "b": 2})
    assert_eq(d.atindex(0), ("a", 1))
    assert_eq(d.atindex(1), ("b", 2))


def test_iterable_indexof():
    d = DictPlus()
    ex(d.indexof, KeyError, "a")
    d.insert(0, ("a", 1))
    assert_eq(d.indexof("a"), 0)


def test_iterable___getitem__():
    d = OrderedDictPlus()
    d.insert(0, ("1", "2"))
    assert_eq(d.get("1"), d["1"])
    assert_eq(d["1"], "2")
    assert_t("1" in d)
    assert_t("5" not in d)
    ex(d.__getitem__, KeyError, "5")


def test_iterable___setitem__():
    d = OrderedDictPlus()
    d.insert(0, ("AAA", "AAA"))
    d["asdf"] = "ghjkl;"
    assert_eq(d, {"asdf": "ghjkl;", "AAA": "AAA"})
    d["asdf"] = "asdf"
    assert_eq(d, {"asdf": "asdf", "AAA": "AAA"})


def test_iterable___contains__():
    d = DictPlus({"a": 1, "b": 2})
    assert_t("a" in d)
    assert_t("b" in d)
    assert_t("c" not in d)


def test_iterable___iter__():
    d = DictPlus({a: a for a in range(0, 10)})
    ii = iter(d)
    iid = iter(d.keys())
    for i in range(0, len(d)):
        assert_eq(next(ii), next(iid))


def test_iterable___len__():
    assert_eq(len(DictPlus()), 0)
    assert_eq(len(DictPlus(a="b")), 1)
    d = DictPlus(a="1", b="2")
    assert_eq(len(d), 2)
    d.popitem()
    assert_eq(len(d), 1)
    d.insert(0, ("c", 3))
    assert_eq(len(d), 2)


def test_iterable___str__():
    assert_eq(str(DictPlus()), str({}))
    assert_eq(str(DictPlus({"a": "b"})), str({"a": "b"}))


def test_iterable___repr__():
    d = DictPlus({a: a ** 3 for a in range(0, 50, 3)})
    assert_eq(eval(repr(d)), d)


def test_iterable_fromkeys():
    ex(Iterable.fromkeys, NotImplementedError, ["a"], 5)


def test_iterable_items():
    d = DictPlus()
    assert_eq(d.items(), list({}.items()))
    d.insert(0, ("a", "b"))
    assert_eq(d.items(), list({"a": "b"}.items()))


def test_iterable_elements():
    d = DictPlus({"a": 1, "b": 2})
    assert_eq(d.elements(), [KeyValuePair("a", 1), KeyValuePair("b", 2)])


def test_iterable_keys():
    d = DictPlus()
    assert_eq(d.keys(), list({}.keys()))
    d.insert(0, ("a", 1))
    d.insert(1, ("b", 2))
    assert_eq(d.keys(), list({"a": 1, "b": 2}.keys()))

    o = {str(a): a for a in range(0, 10)}
    d = DictPlus(o)

    keys = []
    for k in d:
        keys.append(k)
    assert_eq(keys, list(d.keys()))
    assert_eq(keys, list(o.keys()))


def test_iterable_values():
    d = DictPlus()
    assert_eq(d.values(), list({}.values()))
    d.insert(0, ("a", 1))
    d.insert(1, ("b", 2))
    assert_eq(d.values(), list({"a": 1, "b": 2}.values()))


def test_iterable_setdefault():
    d = DictPlus()
    d2 = {}
    assert_eq(d.setdefault("a", 1), d2.setdefault("a", 1))
    assert_eq(d, d2)
    assert_eq(d.setdefault("b"), d2.setdefault("b"))
    assert_eq(d, d2)


def test_iterable_todict():
    d = DictPlus()
    assert_eq(d.todict(), {})
    d.insert(0, ("1", "2"))
    assert_eq(d.todict(), {"1": "2"})
    assert_eq(d, d.todict())
    assert_eq(d, d.copy().todict())


def test_iterable_tolist():
    d = DictPlus()
    assert_eq(d.tolist(), [])
    d.insert(0, ("1", "2"))
    assert_eq(d.tolist(), [("1", "2")])
    assert_eq(d.tolist(), DictPlus(d.tolist()).tolist())
    assert_eq(d.tolist(), d.copy().tolist())


def test_iterable_swap():
    d = DictPlus({"a": {"aa": 1}, "b": {"bb": 2}})
    d.swap("a", "b")
    assert_eq(d.get("a"), {"bb": 2})
    assert_eq(d.get("b"), {"aa": 1})


def test_iterable_clear():
    d = DictPlus({"a": 1})
    assert_eq(d, {"a": 1})
    d.clear()
    assert_eq(d, {})


def test_iterable_update():
    def subtest_iterable_update(e, **kwargs):
        d = DictPlus()
        d.insert(0, ("1", "2"))
        d.update(e, **kwargs)
        assert_eq(d, {"1": "2", **dict(e), **kwargs})
        d.update({"1": "asdf"})
        assert_eq(d, {"1": "asdf", **dict(e), **kwargs})
        assert_eq(d.keys(), ["1"] + list(dict(e).keys()) + list(kwargs.keys()))
        assert_eq(d.values(), ["asdf"] + list(dict(e).values()) + list(kwargs.values()))

    subtest_iterable_update({"21": "12", "Y": "YZ"})
    subtest_iterable_update([("21", "12"), ("Y", "YZ")])
    subtest_iterable_update({"21": "12", "Y": "YZ"}, a="meow", b="cat")
    subtest_iterable_update([("21", "12"), ("Y", "YZ")], a="meow", b="cat")


def test_iterable_unupdate():
    def subtest_iterable_unupdate(e, ee, **kwargs):
        d = OrderedDictPlus()
        d.insert(0, ("1", "2"))
        d.update(e, **kwargs)
        assert_eq(d, {"1": "2", **dict(e), **kwargs})
        d.unupdate(e, **kwargs)
        assert_eq(d, {"1": "2"})

        ex(d.unupdate, KeyError, e, **kwargs)
        d.update(e, **kwargs)
        ex(d.unupdate, InvalidElementValueException, ee, **kwargs)

    subtest_iterable_unupdate({"gg": "ez"}, {"gg": "wp"}, a="meow", b="cat")
    subtest_iterable_unupdate({"gg": "ez"}, {"gg": "wp"})
    subtest_iterable_unupdate([("gg", "ez")], [("gg", "wp")], a="meow", b="cat")
    subtest_iterable_unupdate([("gg", "ez")], [("gg", "wp")])

    d = OrderedDictPlus()
    d.insert(0, ("1", "2"))
    d.insert(-1, ("A", "B"))

    ex(d.unupdate, ValueError, ("A", "B"))


def test_iterable_map():
    d = OrderedDictPlus()
    d["a"] = 1
    d.update({"b": 2, "c": 3})

    def func_e2e(k, v):
        return str(k) + "a", v * 2

    def invfunc_e2e(k, v):
        return str(k)[:-1], v / 2

    od = d.copy()
    d.map(func_e2e)
    assert_eq(d, {"aa": 2, "ba": 4, "ca": 6})
    assert_eq(d.get("aa"), 2)
    d.map(invfunc_e2e)
    assert_eq(d, od)
    assert_eq(d.get("a"), 1)


def test_iterable_rekey():
    def func_k2k(k):
        return k + "a"

    def invfunc_k2k(k):
        return k[:-1]

    o = {"a": 1, "b": 2}
    d = DictPlus(o)
    d.rekey(func_k2k)
    assert_eq(d, {"aa": 1, "ba": 2})
    assert_eq(d.get("aa"), 1)
    d.rekey(invfunc_k2k)
    assert_eq(d.get("a"), 1)
    assert_eq(d, o)


def test_iterable_chop():
    o = {
        0: "a", 1: "b", 2: "c",
        3: "d", 4: "e", 5: "f",
        6: "g", 7: "h"
    }
    d = DictPlus(o)

    def func_chop(k, v):
        return int(k % 2 != 0)

    chopped = d.chop(func_chop)
    assert_eq(chopped[0], {0: "a", 2: "c", 4: "e", 6: "g"})
    assert_eq(chopped[1], {1: "b", 3: "d", 5: "f", 7: "h"})
    d2 = DictPlus()
    d2.update(chopped[0])
    d2.update(chopped[1])
    assert_eq(d2, o)
    assert_eq(chopped[0].__class__, DictPlus)
    assert_eq(chopped[1].__class__, DictPlus)


def test_iterable_squish():
    d = DictPlus({"1": "8", "asdf": "[E]"})

    d.squish(["1", "asdf"], "tt", lambda x: x[0] + x[1])
    assert_eq(d, {"tt": "8[E]"})


def test_iterable_expand():
    o = {"tt": "8[E]"}
    o2 = {"1": "8", "asdf": "[E]"}

    d = DictPlus({"1": "8", "asdf": "[E]"})
    d.squish(["1", "asdf"], "tt", lambda x: x[0] + x[1])
    assert_eq(d, o)

    d.expand("tt", ["1", "asdf"], lambda x: (x[0], x[1:]))
    assert_eq(d, o2)
    ex(d.expand, IndexError, "asdf", ["a", "sdf"], lambda x: x)


def test_iterable_funcmap():
    o = {a: a for a in range(0, 100)}
    o2 = {a: a for a in range(0, 100)}

    def subtest_funcmap(inplace):
        def subsubtest_funcmap(result, expected, returned):
            if inplace:
                assert_eq(result, expected)
                assert_eq(result, returned)
            else:
                assert_eq(result, o)
                assert_eq(returned, expected)

        # Basic test
        d = DictPlus(o)
        dp = d.funcmap(
            o2,
            lambda _v1, _v2: _v1,
            lambda _id: _id,
            inplace=inplace
        )
        subsubtest_funcmap(d, o, dp)

        # Test with nontrivial f
        d = DictPlus(o)
        dp = d.funcmap(
            o2,
            lambda _v1, _v2: _v1 * _v2,
            lambda _id: _id,
            inplace=inplace
        )
        subsubtest_funcmap(d, {a: a * a for a in range(0, 100)}, dp)

        # Test with nontrivial f and g
        d = DictPlus(o)
        dp = d.funcmap(
            o2,
            lambda _v1, _v2: _v1 * _v2,
            lambda _id: 99 - _id,
            inplace=inplace
        )
        subsubtest_funcmap(d, {a: a * (99 - a) for a in range(0, 100)}, dp)

        # Test with scaled g
        d = DictPlus(o)
        dp = d.funcmap(
            {a * 2: 1 / a if a else 0 for a in range(0, 100)},
            lambda _v1, _v2: round(_v1 * _v2),
            lambda _id: _id * 2,
            inplace=inplace
        )
        subsubtest_funcmap(d, {a: 1 if a else 0 for a in range(0, 100)}, dp)

        # Test with len(d) > len(other)
        d = DictPlus(o)
        dp = d.funcmap(
            {a: " % 50 = " + str(a) for a in range(0, 50)},
            lambda _v1, _v2: str(_v1) + _v2,
            lambda _id: _id % 50,
            inplace=inplace
        )

        subsubtest_funcmap(d, {a: "{} % 50 = {}".format(a, a % 50) for a in range(0, 100)}, dp)

        # Test with len(d) < len(other)
        d = DictPlus(o)
        dp = d.funcmap(
            {a: a for a in range(0, 200)},
            lambda _v1, _v2: (_v1 * 2) / _v2 if _v2 else 1,
            lambda _id: _id * 2,
            inplace=inplace
        )

        subsubtest_funcmap(d, {a: 1 for a in range(0, 100)}, dp)

    subtest_funcmap(True)
    subtest_funcmap(False)


def subtest_iterable_fold(fold_func):
    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    def func2_ee2e(*es):
        return KeyValuePair(es[0].id + es[1].id, es[0].value + es[1].value)

    def subsubtest_iterable_fold(di):
        g = getattr(di, fold_func)(func_ee2e)
        gp = getattr(di, fold_func)(func2_ee2e)
        assert_eq(gp, g)
        return g

    d = DictPlus()
    assert_eq(subsubtest_iterable_fold(d), {})
    d.insert(0, (1, 1))
    assert_eq(subsubtest_iterable_fold(d), {1: 1})
    d.insert(1, (2, 2))
    assert_eq(subsubtest_iterable_fold(d), {3: 3})


def test_iterable_fold_left():
    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    subtest_iterable_fold("fold_left")
    d = DictPlus()
    d.update([(0, "a"), (1, "b"), (2, "c")])
    r = d.fold_left(func_ee2e)
    assert_neq(r, d.fold_right(func_ee2e))
    assert_eq(r, {3: "abc"})


def test_iterable_fold_right():
    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    subtest_iterable_fold("fold_right")
    d = DictPlus()
    d.update([(0, "a"), (1, "b"), (2, "c")])
    r = d.fold_right(func_ee2e)
    assert_eq(r, {3: "cba"})


def test_iterable_add():
    o1 = {"a": 1, "b": 2}
    o2 = {"c": 3, "d": 4}
    o3 = {"a": 1, "b": 2, "c": 3, "d": 4}
    d1 = OrderedDictPlus(o1)
    d2 = OrderedDictPlus(o2)
    d3 = OrderedDictPlus(o3)

    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    tt = d1.add(d2)
    assert_eq(tt, d3)
    assert_eq(d1, d3)
    d1 = OrderedDictPlus(o1)
    assert_eq(d1.add(d2, func_ee2e), {"ac": 4, "bd": 6})
    d1 = OrderedDictPlus(o1)
    d1.insert(len(d1), ("g", 6))
    assert_eq(d1.add(o2, func_ee2e), {"ac": 4, "bd": 6, "g": 6})


def test_iterable___add__():
    o1 = {"a": 1, "b": 2}
    o2 = {"c": 3, "d": 4}

    o3 = o1.copy()
    o3.update(o2)

    d1 = DictPlus(o1)
    d2 = DictPlus(o2)
    d3 = d1 + d2

    assert_eq(d1 + d2, d3)
    assert_eq(d1 + d2, o3)
    assert_eq(d1 + o2, o3)
    assert_eq(d2 + o1, o3)


def test_iterable_sub():
    o1 = {"a": 1, "b": 2}
    o2 = {"c": 3, "d": 4}
    o3 = {"a": 1, "b": 2, "c": 3, "d": 4}
    d1 = OrderedDictPlus(o1)
    d2 = OrderedDictPlus(o2)
    d3 = OrderedDictPlus(o3)

    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    def func_inv_ee2e(e1, e2):
        return e1.id[:-1], e1.value - e2.value

    assert_eq(d3.sub(d2), d1)
    d3 = OrderedDictPlus(o3)
    assert_eq(d3.sub(d1), d2)
    assert_eq(d2, d3)
    assert_eq(d3.add(d1), o3)

    assert_eq(d1.add(d2, func_ee2e), {"ac": 4, "bd": 6})
    assert_eq(d1.sub(d2, func_inv_ee2e), o1)
    d1.insert(len(d1), ("g", 6))
    assert_eq(d1.add(d2, func_ee2e), {"ac": 4, "bd": 6, "g": 6})
    assert_eq(d1.sub(d2, func_inv_ee2e), {"a": 1, "b": 2, "g": 6})
    d1.pop("g")
    assert_eq(d1, o1)
    assert_eq(d2, o2)
    assert_eq(d3, o3)


def test_iterable___sub__():
    o1 = {"a": 1, "b": 2}
    o2 = {"c": 3, "d": 4}

    o3 = o1.copy()
    o3.update(o2)

    d3 = DictPlus(o3)
    d2 = DictPlus(o2)
    d1 = DictPlus(o1)

    assert_eq(d3 - d2, d1)
    assert_eq(d3 - o2, o1)
    assert_eq((d3 - o2) - o1, {})
    ex(d3.__sub__, KeyError, {"g": 5})
    ex(d3.__sub__, KeyError, {"a": 20})

    assert_eq(d1, o1)
    assert_eq(d2, o2)
    assert_eq(d3, o3)


def test_iterable_multiply():
    o = {"a": 1, "b": 2, "c": 3}
    d = OrderedDictPlus(o)

    d.multiply({})
    assert_eq(d, {})
    d = OrderedDictPlus(o)

    d.multiply(o)
    assert_eq(d, {
        ("a", "a"): (1, 1), ("a", "b"): (1, 2), ("a", "c"): (1, 3),
        ("b", "a"): (2, 1), ("b", "b"): (2, 2), ("b", "c"): (2, 3),
        ("c", "a"): (3, 1), ("c", "b"): (3, 2), ("c", "c"): (3, 3)
    })
    d = OrderedDictPlus(o)
    d.multiply(o, lambda e1, e2: e1)
    assert_eq(d, o)
    d.multiply(o, lambda e1, e2: (e1.id + e2.id, (e1.value, e2.value)))
    assert_eq(d, {
        "aa": (1, 1), "ab": (1, 2), "ac": (1, 3),
        "ba": (2, 1), "bb": (2, 2), "bc": (2, 3),
        "ca": (3, 1), "cb": (3, 2), "cc": (3, 3)
    })


def test_iterable___mul__():
    o = {"a": 1, "b": 2, "c": 3}
    d = OrderedDictPlus(o)

    assert_eq(d * {}, {})
    assert_eq(d, o)

    assert_eq(d * o, {
        ("a", "a"): (1, 1), ("a", "b"): (1, 2), ("a", "c"): (1, 3),
        ("b", "a"): (2, 1), ("b", "b"): (2, 2), ("b", "c"): (2, 3),
        ("c", "a"): (3, 1), ("c", "b"): (3, 2), ("c", "c"): (3, 3)
    })


def test_iterable_divide():
    o = {
        ("a", "a"): (1, 1), ("a", "b"): (1, 2), ("a", "c"): (1, 3),
        ("b", "a"): (2, 1), ("b", "b"): (2, 2), ("b", "c"): (2, 3),
        ("c", "a"): (3, 1), ("c", "b"): (3, 2), ("c", "c"): (3, 3)
    }
    o2 = {"a": 1, "b": 2, "c": 3}
    d = OrderedDictPlus(o)
    d.divide(o, lambda el, e2: (el.id[0], el.value[0]))
    assert_eq(d, o2)

    d.multiply(o2)
    assert_eq(d, o)
    d.divide(o2)
    assert_eq(d, o2)


def test_iterable___truediv__():
    o = {
        ("a", "a"): (1, 1), ("a", "b"): (1, 2), ("a", "c"): (1, 3),
        ("b", "a"): (2, 1), ("b", "b"): (2, 2), ("b", "c"): (2, 3),
        ("c", "a"): (3, 1), ("c", "b"): (3, 2), ("c", "c"): (3, 3)
    }
    o2 = {"a": 1, "b": 2, "c": 3}
    d = OrderedDictPlus(o2)
    assert_eq(d * d, o)
    assert_eq((d * d) / d, d)


def test_iterable___le__():
    ao = {0: 0, 1: 1}
    bo = {2: 2, 3: 3}

    ad = OrderedDictPlus(ao)
    bd = OrderedDictPlus(bo)

    assert_op(ad, bd, operator.le)
    assert_eq(ad, ao)
    assert_eq(bd, bo)

    assert_op(ad, ad, operator.le)
    assert_op(bd, bd, operator.le)
    assert_eq(ad, ao)
    assert_eq(bd, bo)


def test_iterable___lt__():
    ao = {0: 0, 1: 1}
    bo = {2: 2, 3: 3}

    ad = OrderedDictPlus(ao)
    bd = OrderedDictPlus(bo)

    assert_op(ad, bd, operator.lt)
    assert_nop(bd, ad, operator.lt)
    assert_eq(ad, ao)
    assert_eq(bd, bo)

    assert_nop(ad, ad, operator.lt)
    assert_nop(bd, bd, operator.lt)
    assert_eq(ad, ao)
    assert_eq(bd, bo)


def test_iterable___ge__():
    ao = {0: 0, 1: 1}
    bo = {2: 2, 3: 3}

    ad = OrderedDictPlus(ao)
    bd = OrderedDictPlus(bo)

    assert_op(bd, ad, operator.ge)
    assert_nop(ad, bd, operator.ge)
    assert_eq(ad, ao)
    assert_eq(bd, bo)

    assert_op(ad, ad, operator.ge)
    assert_op(bd, bd, operator.ge)
    assert_eq(ad, ao)
    assert_eq(bd, bo)


def test_iterable___gt__():
    ao = {0: 0, 1: 1}
    bo = {2: 2, 3: 3}

    ad = OrderedDictPlus(ao)
    bd = OrderedDictPlus(bo)

    assert_op(bd, ad, operator.gt)
    assert_nop(ad, bd, operator.gt)
    assert_eq(ad, ao)
    assert_eq(bd, bo)

    assert_nop(ad, ad, operator.gt)
    assert_nop(bd, bd, operator.gt)
    assert_eq(ad, ao)
    assert_eq(bd, bo)


##################


def test_orderediterable_insert():
    d = OrderedDictPlus()
    assert_eq(d.insert(0, ("a", "b")), KeyValuePair("a", "b"))
    assert_eq(d.insert(1, ("b", "c")), ("b", "c"))
    assert_eq(d.insert(5, KeyValuePair("g", "h")), KeyValuePair("g", "h"))
    assert_eq(d.insert(0, KeyValuePair("e", "f")), ("e", "f"))
    assert_eq(d, {"a": "b", "b": "c", "g": "h", "e": "f"})
    assert_eq(d.values(), ["f", "b", "c", "h"])
    assert_eq(d.keys(), ["e", "a", "b", "g"])
    ex(d.insert, InvalidElementTypeException, 0, "meow")


def test_orderediterable_pop():
    d = OrderedDictPlus()
    d.insert(0, ("1", "2"))
    assert_eq(d.pop("1"), "2")
    assert_eq(d.pop("1", "2"), "2")


#################


def test_dictplus___eq__():
    d = DictPlus()
    d.insert(0, (0, "asdf"))
    d.insert(1, (1, "fdsa"))

    d2 = DictPlus()
    d2.insert(0, (1, "fdsa"))
    d2.insert(1, (0, "asdf"))

    assert_neq(d, 8)
    assert_neq(d2, 8)
    assert_eq(d, {1: "fdsa", 0: "asdf"})
    assert_eq(d2, {1: "fdsa", 0: "asdf"})
    assert_eq(d, d2)
    assert_eq(DictPlus(), {})
    assert_neq(DictPlus(), [])

    d3 = OrderedDictPlus({1: "fdsa", 0: "asdf"})
    assert_eq(d, d3)  # DictPlus doesn't care about order
    assert_neq(d3, d)  # OrderedDictPlus does

    d4 = OrderedDictPlus()
    d4.insert(0, (0, "asdf"))
    d4.insert(1, (1, "fdsa"))
    assert_eq(d, d4)
    assert_eq(d4, d)


def test_dictplus_fromkeys():
    assert_eq(dict.fromkeys(["a", "b", "c"]), DictPlus.fromkeys(["a", "b", "c"]))
    assert_eq(dict.fromkeys(["a", "b", "c"], 10), DictPlus.fromkeys(["a", "b", "c"], 10))


##################


def test_ordereddictplus___init__():
    def subtest_ordereddictplus__init__(data):
        d = OrderedDictPlus(data=data)
        assert_eq(d, data)
        assert_eq(OrderedDictPlus(data={"v": data}), {"v": data})

    assert_neq(OrderedDictPlus(), [])
    assert_eq(OrderedDictPlus(), {})
    assert_eq(OrderedDictPlus([]), {})
    assert_eq(OrderedDictPlus({}), {})
    assert_eq(OrderedDictPlus(OrderedDictPlus()), {})
    assert_eq(OrderedDictPlus([("a", 1), ("b", 2)]), {"a": 1, "b": 2})
    subtest_ordereddictplus__init__(OrderedDictPlus())
    subtest_ordereddictplus__init__({})
    subtest_ordereddictplus__init__({"a": 1, "b": 2})


def test_ordereddictplus___eq__():
    d = OrderedDictPlus()

    d.insert(0, (0, "asdf"))
    d.insert(1, (1, "fdsa"))

    d2 = OrderedDictPlus()
    d2.insert(0, (1, "fdsa"))
    d2.insert(1, (0, "asdf"))

    assert_neq(d, 8)
    assert_eq(d, {1: "fdsa", 0: "asdf"})
    assert_eq(d2, {1: "fdsa", 0: "asdf"})
    assert_neq(d, d2)
    assert_eq(OrderedDictPlus(), {})
    assert_neq(OrderedDictPlus(), [])

    d3 = DictPlus({1: "fdsa", 0: "asdf"})
    assert_neq(d, d3)
    assert_eq(d3, d)


def test_ordereddictplus_fromkeys():
    assert_eq(dict.fromkeys(["a", "b", "c"]), DictPlus.fromkeys(["a", "b", "c"]))
    assert_eq(dict.fromkeys(["a", "b", "c"], 10), DictPlus.fromkeys(["a", "b", "c"], 10))


###############
def test_functionallyinsensitivedictplus___init__():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus()
    d = FunctionallyInsensitiveDictPlus(comp_func)
    d["a"] = 5
    assert_eq(d["a"], d["1a"])


def test_functionallyinsensitivedictplus__find_base_key():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(comp_func)
    d["a"] = 5
    assert_eq(d._find_base_key("1a"), "a")


def test_functionallyinsensitivedictplus_getitem():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(comp_func)
    d["a"] = 5
    assert_eq(d.getitem("a"), d.getitem("1a"))
    ex(d.getitem, KeyError, "asdf")

def test_functionallyinsensitivedictplus_pop():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(comp_func)
    d["a"] = 5
    assert_eq(d.pop("1a"), 5)
    assert_eq(d.pop("1b", 2), 2)
    ex(d.pop, KeyError, "a")


def test_functionallyinsensitivedictplus_update():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(comp_func)
    d["a"] = 5
    d2 = {"1a": 6, "b": 2}
    d.update(d2)
    assert_eq(d["a"], 6)
    assert_eq(d["b"], 2)


def test_functionallyinsensitivedictplus_indexof():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(comp_func)
    d["a"] = 5
    assert_eq(d.indexof("1a"), d.indexof("a"))


def test_functionallyinsensitivedictplus_setdefault():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(comp_func)
    d["a"] = 5
    assert_eq(d.setdefault("1a"), ("a", 5))
    assert_eq(d.setdefault("b", 2),  2)


def test_functionallyinsensitivedictplus___contains__():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(comp_func)
    d["a"] = 5
    assert_t("a" in d)
    assert_t("1a" in d)
    assert_f("b" in d)


def test_functionallyinsensitivedictplus___setitem__():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(comp_func)
    d["a"] = 5
    d["a"] = 4
    assert_eq(d["a"], 4)
    assert_eq(d["1a"], 4)
    d["1a"] = 2
    assert_eq(d["a"], 2)
    assert_eq(d["1a"], 2)


def test_caseinsensitivedictplus___init__():
    d = CaseInsensitiveDictPlus()
    d["a"] = 5
    assert_eq(d["A"], 5)
    assert_eq(d["a"], 5)
    d["A"] = 4
    assert_eq(d["A"], 4)
    assert_eq(d["a"], 4)


def test_prefixinsensitivedictplus___init__():
    d = PrefixInsensitiveDictPlus(["http://", "https://"])
    d["google.com"] = 5
    assert_eq(d["http://google.com"], 5)
    assert_eq(d["https://google.com"], 5)

    d["http://google.com"] = 4
    assert_eq(d["google.com"], 4)
    assert_eq(d["https://google.com"], 4)


def test_suffixinsensitivedictplus___init__():
    d = SuffixInsensitiveDictPlus([".com",  ".net"])
    d["google"] = 5
    assert_eq(d["google.net"], 5)
    assert_eq(d["google.com"], 5)

    d["google.net"] = 4
    assert_eq(d["google"], 4)
    assert_eq(d["google.com"], 4)


tests = [
    # IterableIndex tests
    test_iterableindex,

    # KeyValuePair tests
    test_keyvaluepair_parse_object,
    test_keyvaluepair___eq__,

    # Element tests
    test_element___init__,
    test_element_parts,
    test_element___eq__,

    # Iterable tests
    test_iterable_get,
    test_iterable_getitem,
    test_iterable_insert,
    test_iterable_pop,
    test_iterable_popitem,
    test_iterable_copy,
    test_iterable_atindex,
    test_iterable_indexof,
    test_iterable___setitem__,
    test_iterable___getitem__,
    test_iterable___contains__,
    test_iterable___iter__,
    test_iterable___len__,
    test_iterable___str__,
    test_iterable___repr__,
    test_iterable_fromkeys,
    test_iterable_items,
    test_iterable_elements,
    test_iterable_keys,
    test_iterable_values,
    test_iterable_setdefault,
    test_iterable_todict,
    test_iterable_tolist,
    test_iterable_swap,
    test_iterable_clear,
    test_iterable_update,
    test_iterable_unupdate,
    test_iterable_map,
    test_iterable_rekey,
    test_iterable_chop,
    test_iterable_squish,
    test_iterable_expand,
    test_iterable_funcmap,
    test_iterable_fold_left,
    test_iterable_fold_right,
    test_iterable_add,
    test_iterable___add__,
    test_iterable_sub,
    test_iterable___sub__,
    test_iterable_multiply,
    test_iterable___mul__,
    test_iterable_divide,
    test_iterable___truediv__,
    test_iterable___le__,
    test_iterable___lt__,
    test_iterable___ge__,
    test_iterable___gt__,

    # OrderedIterable tests
    test_orderediterable_insert,
    test_orderediterable_pop,

    # DictPlus tests
    test_dictplus___eq__,
    test_dictplus_fromkeys,

    # OrderedDictPlus tests
    test_ordereddictplus___init__,
    test_ordereddictplus___eq__,
    test_ordereddictplus_fromkeys,

    # FunctionallyInsensitiveDictPlus tests
    test_functionallyinsensitivedictplus___init__,
    test_functionallyinsensitivedictplus__find_base_key,
    test_functionallyinsensitivedictplus_getitem,
    test_functionallyinsensitivedictplus_pop,
    test_functionallyinsensitivedictplus_update,
    test_functionallyinsensitivedictplus_indexof,
    test_functionallyinsensitivedictplus_setdefault,
    test_functionallyinsensitivedictplus___contains__,
    test_functionallyinsensitivedictplus___setitem__,

    # CaseInsensitiveDictPlus tests
    test_caseinsensitivedictplus___init__,

    # PrefixInsensitiveDictPlus tests
    test_prefixinsensitivedictplus___init__,

    # SuffixInsensitiveDictPlus tests
    test_suffixinsensitivedictplus___init__
]

results = {}
pass_count = 0
total_count = 0

for test in tests:
    name = getattr(test, "__name__")
    try:
        test()
        results[name] = "Passed"
        pass_count = pass_count + 1
    except Exception as e:
        results[name] = "{}: {}".format(e.__class__.__name__, str(e))
        # if e.__class__ != NotImplementedError:
        raise e
    total_count = total_count + 1

for k, v in results.items():
    print("{}:\n{}\n".format(k, v))

print("Passed: {} Total: {} - {}%".format(pass_count, total_count, round((pass_count / total_count), 4)))

total = 0
for k, v in assertions.items():
    print("-- {}: {}".format(k, v))
    total = total + v
print("Total: {}".format(total))
