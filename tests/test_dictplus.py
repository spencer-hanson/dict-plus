# import sys, os
# myPath = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, myPath + '/../')
#
import pytest
from dict_plus.dictplus import *
from dict_plus.insensitive import *
from dict_plus.indexes import IterableIndex, SortedIterableIndex
from dict_plus import *
from dict_plus.exceptions import *
import operator
import six

assertions = {
    "op": 0,
    "nop": 0,
    "eq": 0,
    "neq": 0,
    "t": 0,
    "f": 0
}
index_types = [IterableIndex, SortedIterableIndex]

unsorted_dict_types = [DictPlus, OrderedDictPlus, SuffixInsensitiveDictPlus, PrefixInsensitiveDictPlus,
                       CaseInsensitiveDictPlus, FunctionallyInsensitiveDictPlus]

sorted_dict_types = [SortedDictPlus]

unordered_dict_types = [DictPlus, SuffixInsensitiveDictPlus, PrefixInsensitiveDictPlus,
                        CaseInsensitiveDictPlus, FunctionallyInsensitiveDictPlus]

ordered_dict_types = [OrderedDictPlus]

all_dict_types = list(unsorted_dict_types)
all_dict_types.extend(sorted_dict_types)
all_dict_types.extend(ordered_dict_types)
all_dict_types.extend(unordered_dict_types)

all_dict_types = list(set(all_dict_types))


el_types = [ElementFactory.element(el, ds) for ds in all_dict_types for el in [KeyValuePair]]


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


class A(object):
    pass


class B(object):
    __hash__ = None


@pytest.mark.parametrize("data", [
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
])
@pytest.mark.parametrize("index_type", index_types)
def test_iterableindex(index_type, data):
    ii = index_type()

    things_to_hash = [data, [data], [1, data]]

    for idx, thing in enumerate(things_to_hash):
        ii.set(thing, idx)
        ii.get(thing)


@pytest.mark.parametrize("_id", ["a", u"b", 1])
@pytest.mark.parametrize("val", ["a", u"b", 2])
@pytest.mark.parametrize("eltyp", el_types)
@pytest.mark.parametrize("dtyp", all_dict_types)
def test_keyvaluepair_parse_object(_id, val, eltyp, dtyp):
    parse = ElementFactory.element(eltyp, dtyp)

    ex(parse, InvalidElementTypeException, (_id, _id, _id))
    ex(parse, InvalidElementTypeException, (val, val, val))

    assert_eq(parse((_id, val)), (_id, val))
    assert_eq(parse((val, _id)), (val, _id))

    assert_eq(parse(KeyValuePair(_id, val)), (_id, val))
    assert_eq(parse(KeyValuePair(val, _id)), (val, _id))


@pytest.mark.parametrize("eltyp", el_types)
def test_keyvaluepair___eq__(eltyp):
    assert_eq(eltyp("a", "b"), {"a": "b"})
    assert_eq(eltyp("a", "b"), ("a", "b"))
    assert_neq(eltyp("a", "b"), ("b", "a"))
    kvp = eltyp("a", "b")

    assert_eq(kvp, kvp.copy())


##################

@pytest.mark.parametrize("eltyp", el_types)
def test_element___init__(eltyp):
    ex(eltyp, InvalidElementTypeException, "id", None)
    ex(eltyp, TypeError, None, "value")
    assert_eq(eltyp(0, 1), eltyp((0, 1)))
    assert_eq(eltyp(eltyp(0, 1)), eltyp((0, 1)))


@pytest.mark.parametrize("eltyp", el_types)
def test_element_parts(eltyp):
    assert_eq(eltyp(0, 1).parts(), (0, 1))


@pytest.mark.parametrize("dtype", all_dict_types)
def test_element___eq__(dtype):
    d = dtype()
    eltyp = d.elements_type

    d.insert(0, ("4", "3"))
    assert_eq(d.getitem("4"), eltyp("4", "3"))
    assert_eq(("4", "3"), eltyp("4", "3"))
    assert_eq(eltyp("a", "b"), eltyp("a", "b"))
    assert_eq(eltyp("1", "2"), ("1", "2"))
    assert_neq(eltyp("1", "2"), ["1", "2"])
    assert_eq(eltyp("a", "b"), {"a": "b"})
    assert_neq(eltyp("c", "d"), {"a": "b", "c": "d"})


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_get(dtype):
    d = dtype()
    d.insert(0, ("1", "2"))
    assert_eq(d.get("1"), "2")


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_getitem(dtype):
    d = dtype()
    d.insert(0, ("1", "2"))
    assert_neq(d.getitem("1"), 8)
    assert_eq(d.getitem("1"), d.elements_type("1", "2"))


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_insert(dtype):
    d = dtype()
    assert_t(d.insert(12345, ("a", "g")))
    ex(d.insert, KeyError, 12345, ("a", "b"))
    assert_eq(d._indexes.get("a"), 0)
    assert_eq(d._elements[0], ("a", "g"))


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_pop(dtype):
    d = dtype({"a": "b", "c": "d"})
    assert_eq(d.pop("a"), "b")
    assert_eq(d, {"c": "d"})
    d.insert(1, ("a", "b"))
    assert_eq(d.pop("a"), "b")
    assert_eq(d.pop("c"), "d")
    ex(d.pop, KeyError, "a")


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_popitem(dtype):
    d = dtype({"a": "b"})
    t = d.popitem()
    assert_eq(t, ("a", "b"))
    ex(d.popitem, KeyError)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_copy(dtype):
    d = dtype()
    d.insert(0, ("1", "2"))
    c = d.copy()
    assert_eq(d, c)

    d.insert(-1, ("[E]", "no u"))
    assert_neq(d, c)
    d.pop("[E]")
    d["1"] = "1"
    assert_neq(d, c)


@pytest.mark.parametrize("dtype", unsorted_dict_types)
def test_iterable_atindex(dtype):
    d = dtype({"a": 1, "b": 2})
    assert_eq(d.atindex(0), ("a", 1))
    assert_eq(d.atindex(1), ("b", 2))


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_indexof(dtype):
    d = dtype()
    ex(d.indexof, KeyError, "a")
    d.insert(0, ("a", 1))
    assert_eq(d.indexof("a"), 0)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___getitem__(dtype):
    d = dtype()
    d.insert(0, ("1", "2"))
    assert_eq(d.get("1"), d["1"])
    assert_eq(d["1"], "2")
    assert_t("1" in d)
    assert_t("5" not in d)
    ex(d.__getitem__, KeyError, "5")


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___setitem__(dtype):
    d = dtype()
    d.insert(0, ("AAA", "AAA"))
    d["asdf"] = "ghjkl;"
    assert_eq(d, {"asdf": "ghjkl;", "AAA": "AAA"})
    d["asdf"] = "asdf"
    assert_eq(d, {"asdf": "asdf", "AAA": "AAA"})


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___contains__(dtype):
    d = dtype({"a": 1, "b": 2})
    assert_t("a" in d)
    assert_t("b" in d)
    assert_t("c" not in d)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___iter__(dtype):
    d = dtype({a: a for a in range(0, 10)})
    ii = iter(d)
    iid = iter(d.keys())
    for i in range(0, len(d)):
        assert_eq(next(ii), next(iid))


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___len__(dtype):
    assert_eq(len(dtype()), 0)
    assert_eq(len(dtype(a="b")), 1)
    d = dtype(a="1", b="2")
    assert_eq(len(d), 2)
    d.popitem()
    assert_eq(len(d), 1)
    d.insert(0, ("c", 3))
    assert_eq(len(d), 2)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___str__(dtype):
    assert_eq(str(dtype()), str({}))
    assert_eq(str(dtype({"a": "b"})), str({"a": "b"}))


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___repr__(dtype):
    d = dtype({a: a ** 3 for a in range(0, 50, 3)})
    assert_eq(eval(repr(d)), d)


def test_iterable_fromkeys():
    ex(Iterable.fromkeys, NotImplementedError, ["a"], 5)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_items(dtype):
    d = dtype()
    assert_eq(d.items(), list({}.items()))
    d.insert(0, ("a", "b"))
    assert_eq(d.items(), list({"a": "b"}.items()))


@pytest.mark.parametrize("dtype", unsorted_dict_types)
def test_iterable_elements(dtype):
    d = dtype({"a": 1, "b": 2})
    assert_eq(d.elements(), [d.elements_type("a", 1), d.elements_type("b", 2)])


@pytest.mark.parametrize("dtype", unsorted_dict_types)
def test_iterable_keys(dtype):
    d = dtype()
    assert_eq(d.keys(), list({}.keys()))
    d.insert(0, ("a", 1))
    d.insert(1, ("b", 2))
    assert_eq(d.keys(), list({"a": 1, "b": 2}.keys()))

    o = {str(a): a for a in range(0, 10)}
    d = dtype(o)

    keys = []
    for k in d:
        keys.append(k)
    assert_eq(keys, list(d.keys()))
    assert_eq(keys, list(o.keys()))


@pytest.mark.parametrize("dtype", unsorted_dict_types)
def test_iterable_values(dtype):
    d = dtype()
    assert_eq(d.values(), list({}.values()))
    d.insert(0, ("a", 1))
    d.insert(1, ("b", 2))
    assert_eq(d.values(), list({"a": 1, "b": 2}.values()))


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_setdefault(dtype):
    d = dtype()
    d2 = {}
    assert_eq(d.setdefault("a", 1), d2.setdefault("a", 1))
    assert_eq(d, d2)
    assert_eq(d.setdefault("b"), d2.setdefault("b"))
    assert_eq(d, d2)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_todict(dtype):
    d = dtype()
    assert_eq(d.todict(), {})
    d.insert(0, ("1", "2"))
    assert_eq(d.todict(), {"1": "2"})
    assert_eq(d, d.todict())
    assert_eq(d, d.copy().todict())


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_tolist(dtype):
    d = dtype()
    assert_eq(d.tolist(), [])
    d.insert(0, ("1", "2"))
    assert_eq(d.tolist(), [("1", "2")])
    assert_eq(d.tolist(), dtype(d.tolist()).tolist())
    assert_eq(d.tolist(), d.copy().tolist())


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_swap(dtype):
    d = dtype({"a": {"aa": 1}, "b": {"bb": 2}})
    d.swap("a", "b")
    assert_eq(d.get("a"), {"bb": 2})
    assert_eq(d.get("b"), {"aa": 1})


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_clear(dtype):
    d = dtype({"a": 1})
    assert_eq(d, {"a": 1})
    d.clear()
    assert_eq(d, {})


@pytest.mark.parametrize("dtype", all_dict_types)
@pytest.mark.parametrize("e", [{"21": "12", "Y": "YZ"}, [("21", "12")], [("21", "12"), ("Y", "YZ")]])
@pytest.mark.parametrize("kwargs", [{"a": "meow", "b": "cat"}, {}])
def test_iterable_update(dtype, e, kwargs):
    d = dtype()
    d.insert(0, ("1", "2"))
    d.update(e, **kwargs)

    t = {"1": "2"}
    t.update(dict(e))
    t.update(**kwargs)
    assert_eq(d, t)
    d.update({"1": "asdf"})

    t = {"1": "asdf"}
    t.update(dict(e))
    t.update(kwargs)
    assert_eq(d, t)
    l2 = ["1"] + list(dict(e).keys()) + list(kwargs.keys())
    assert_t(all(el in d.keys() for el in l2))
    assert_t(len(d.keys()) == len(l2))

    l3 = ["asdf"] + list(dict(e).values()) + list(kwargs.values())
    assert_t(all(el in d.values() for el in l3))
    assert_t(len(d.values()) == len(l3))


@pytest.mark.parametrize("dtype", all_dict_types)
@pytest.mark.parametrize("e", [{"gg": "wp"}, [("gg", "wp")]])
@pytest.mark.parametrize("ee", [{"gg": "ez"}, [("gg", "ez")]])
@pytest.mark.parametrize("kwargs", [{"a": "meow", "b": "cat"}, {}])
def test_iterable_unupdate(dtype, e, ee, kwargs):
    d = dtype()
    d.insert(0, ("1", "2"))
    d.update(e, **kwargs)

    t = {"1": "2"}
    t.update(dict(e))
    t.update(kwargs)
    assert_eq(d, t)

    d.unupdate(e, **kwargs)
    assert_eq(d, {"1": "2"})

    ex(d.unupdate, KeyError, e, **kwargs)
    d.update(e, **kwargs)
    ex(d.unupdate, InvalidElementValueException, ee, **kwargs)

    d = dtype()
    d.insert(0, ("1", "2"))
    d.insert(-1, ("A", "B"))

    ex(d.unupdate, ValueError, ("A", "B"))


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_map(dtype):
    d = dtype()
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

    def func_broke(k, v):
        return "a", 5

    ex(d.map, IndexError, func_broke)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_filter(dtype):
    d = dtype({"a": 1, "b": 2, "c": 3, "d": 4})
    d.filter(lambda k, v: bool(v % 2))
    assert_eq(d, {"a": 1, "c": 3})


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_rekey(dtype):
    def func_k2k(k):
        return k + "a"

    def invfunc_k2k(k):
        return k[:-1]

    o = {"a": 1, "b": 2}
    d = dtype(o)
    d.rekey(func_k2k)
    assert_eq(d, {"aa": 1, "ba": 2})
    assert_eq(d.get("aa"), 1)
    d.rekey(invfunc_k2k)
    assert_eq(d.get("a"), 1)
    assert_eq(d, o)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_chop(dtype):
    o = {
        0: "a", 1: "b", 2: "c",
        3: "d", 4: "e", 5: "f",
        6: "g", 7: "h"
    }
    d = dtype(o)

    def func_chop(k, v):
        return int(k % 2 != 0)

    chopped = d.chop(func_chop)
    assert_eq(chopped[0], {0: "a", 2: "c", 4: "e", 6: "g"})
    assert_eq(chopped[1], {1: "b", 3: "d", 5: "f", 7: "h"})
    d2 = dtype()
    d2.update(chopped[0])
    d2.update(chopped[1])
    assert_eq(d2, o)
    assert_eq(chopped[0].__class__, dtype)
    assert_eq(chopped[1].__class__, dtype)

    def func_chop2(k, v):
        return "asdf"

    ex(d.chop, ValueError, func_chop2)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_squish(dtype):
    d = dtype({"1": "8", "asdf": "[E]"})

    d.squish(["1", "asdf"], "tt", lambda x: x[0] + x[1])
    assert_eq(d, {"tt": "8[E]"})


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_expand(dtype):
    o = {"tt": "8[E]"}
    o2 = {"1": "8", "asdf": "[E]"}

    d = dtype({"1": "8", "asdf": "[E]"})
    d.squish(["1", "asdf"], "tt", lambda x: x[0] + x[1])
    assert_eq(d, o)

    d.expand("tt", ["1", "asdf"], lambda x: (x[0], x[1:]))
    assert_eq(d, o2)
    ex(d.expand, IndexError, "asdf", ["a", "sdf"], lambda x: x)


def subsubtest_funcmap(inplace, result, expected, returned):
    if inplace:
        assert_eq(result, expected)
        assert_eq(result, returned)
    else:
        assert_eq(result, {a: a for a in range(0, 100)})
        assert_eq(returned, expected)


@pytest.mark.parametrize("dtype", all_dict_types)
@pytest.mark.parametrize("inplace", [True, False])
def test_iterable_funcmap_basic(dtype, inplace):
    o = {a: a for a in range(0, 100)}
    o2 = {a: a for a in range(0, 100)}

    # Basic test
    d = dtype(o)
    dp = d.funcmap(
        o2,
        lambda _v1, _v2: _v1,
        lambda _id: _id,
        inplace=inplace
    )
    subsubtest_funcmap(inplace, d, o, dp)


@pytest.mark.parametrize("dtype", all_dict_types)
@pytest.mark.parametrize("inplace", [True, False])
def test_iterable_funcmap_nontrivial_f(dtype, inplace):
    o = {a: a for a in range(0, 100)}
    o2 = {a: a for a in range(0, 100)}

    # Test with nontrivial f
    d = dtype(o)
    dp = d.funcmap(
        o2,
        lambda _v1, _v2: _v1 * _v2,
        lambda _id: _id,
        inplace=inplace
    )
    subsubtest_funcmap(inplace, d, {a: a * a for a in range(0, 100)}, dp)


@pytest.mark.parametrize("dtype", all_dict_types)
@pytest.mark.parametrize("inplace", [True, False])
def test_iterable_funcmap_nontrivial_fg(dtype, inplace):
    o = {a: a for a in range(0, 100)}
    o2 = {a: a for a in range(0, 100)}

    # Test with nontrivial f and g
    d = dtype(o)
    dp = d.funcmap(
        o2,
        lambda _v1, _v2: _v1 * _v2,
        lambda _id: 99 - _id,
        inplace=inplace
    )
    subsubtest_funcmap(inplace, d, {a: a * (99 - a) for a in range(0, 100)}, dp)


@pytest.mark.parametrize("dtype", all_dict_types)
@pytest.mark.parametrize("inplace", [True, False])
def test_iterable_funcmap_scaled(dtype, inplace):
    o = {a: a for a in range(0, 100)}

    # Test with scaled g
    d = dtype(o)
    dp = d.funcmap(
        {a * 2: 1 / float(a) if a else 0 for a in range(0, 100)},
        lambda _v1, _v2: round(_v1 * _v2),
        lambda _id: _id * 2,
        inplace=inplace
    )
    subsubtest_funcmap(inplace, d, {a: 1 if a else 0 for a in range(0, 100)}, dp)


@pytest.mark.parametrize("dtype", all_dict_types)
@pytest.mark.parametrize("inplace", [True, False])
def test_iterable_funcmap_d_gt(dtype, inplace):
    o = {a: a for a in range(0, 100)}

    # Test with len(d) > len(other)
    d = dtype(o)
    dp = d.funcmap(
        {a: " % 50 = " + str(a) for a in range(0, 50)},
        lambda _v1, _v2: str(_v1) + _v2,
        lambda _id: _id % 50,
        inplace=inplace
    )

    subsubtest_funcmap(inplace, d, {a: "{} % 50 = {}".format(a, a % 50) for a in range(0, 100)}, dp)


@pytest.mark.parametrize("dtype", all_dict_types)
@pytest.mark.parametrize("inplace", [True, False])
def test_iterable_funcmap_d_gl(dtype, inplace):
    o = {a: a for a in range(0, 100)}

    # Test with len(d) < len(other)
    d = dtype(o)
    dp = d.funcmap(
        {a: a for a in range(0, 200)},
        lambda _v1, _v2: (_v1 * 2) / _v2 if _v2 else 1,
        lambda _id: _id * 2,
        inplace=inplace
    )

    subsubtest_funcmap(inplace, d, {a: 1 for a in range(0, 100)}, dp)


@pytest.mark.parametrize("dtype", unsorted_dict_types)
@pytest.mark.parametrize("fold_type", [("fold_left", {3: "abc"}), ("fold_right", {3: "cba"})])
@pytest.mark.parametrize("vals", [
    ({}, []),
    ({1: 1}, [(0, (1, 1))]),
    ({3: 3}, [(0, (1, 1)), (1, (2, 2))]),
])
def test_iterable_folds(dtype, fold_type, vals):
    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    def func2_ee2e(*es):
        return KeyValuePair(es[0].id + es[1].id, es[0].value + es[1].value)

    val, data = vals

    fn_name, result = fold_type

    # def subsubtest_iterable_fold(di):
    #     g = getattr(di, fn_name)(func_ee2e)
    #     gp = getattr(di, fn_name)(func2_ee2e)
    #     assert_eq(gp, g)
    #     return g

    d = dtype()
    for da in data:
        d.insert(*da)

    # assert_eq(subsubtest_iterable_fold(d), {})
    g = getattr(d, fn_name)(func_ee2e)
    gp = getattr(d, fn_name)(func2_ee2e)
    assert_eq(gp, g)
    assert_eq(g, val)

    # d.insert(0, (1, 1))
    # assert_eq(subsubtest_iterable_fold(d), {1: 1})
    # d.insert(1, (2, 2))
    # assert_eq(subsubtest_iterable_fold(d), {3: 3})

    d = dtype()
    d.update([(0, "a"), (1, "b"), (2, "c")])
    r = getattr(d, fn_name)(func_ee2e)
    assert_eq(r, result)


@pytest.mark.parametrize("dtype", unsorted_dict_types)
def test_iterable_add(dtype):
    o1 = {"a": 1, "b": 2}
    o2 = {"c": 3, "d": 4}
    o3 = {"a": 1, "b": 2, "c": 3, "d": 4}
    d1 = dtype(o1)
    d2 = dtype(o2)
    if six.PY2:  # Python 2 dictionaries aren't created in order as defined, ie o3/d3 in py2 is acdb
        d3 = dtype({"a": 1, "b": 2})
        d3 = d3 + {"c": 3}
        d3 += {"d": 4}
    else:
        d3 = dtype(o3)

    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    tt = d1.add(d2)
    assert_eq(tt, d3)
    assert_eq(d1, d3)
    d1 = dtype(o1)
    assert_eq(d1.add(d2, func_ee2e), {"ac": 4, "bd": 6})
    d1 = dtype(o1)
    d1.insert(len(d1), ("g", 6))
    assert_eq(d1.add(o2, func_ee2e), {"ac": 4, "bd": 6, "g": 6})


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___add__(dtype):
    o1 = {"a": 1, "b": 2}
    o2 = {"c": 3, "d": 4}

    o3 = o1.copy()
    o3.update(o2)

    d1 = dtype(o1)
    d2 = dtype(o2)
    d3 = d1 + d2

    assert_eq(d1 + d2, d3)
    assert_eq(d1 + d2, o3)
    assert_eq(d1 + o2, o3)
    assert_eq(d2 + o1, o3)


@pytest.mark.parametrize("dtype", unsorted_dict_types)
def test_iterable_sub(dtype):
    o1 = {"a": 1, "b": 2}
    o2 = {"c": 3, "d": 4}
    o3 = {"a": 1, "b": 2, "c": 3, "d": 4}
    d1 = dtype(o1)
    d2 = dtype(o2)
    d3 = dtype(o3)

    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    def func_inv_ee2e(e1, e2):
        return e1.id[:-1], e1.value - e2.value

    assert_eq(d3.sub(d2), d1)
    d3 = dtype(o3)
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


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___sub__(dtype):
    o1 = {"a": 1, "b": 2}
    o2 = {"c": 3, "d": 4}

    o3 = o1.copy()
    o3.update(o2)

    d3 = dtype(o3)
    d2 = dtype(o2)
    d1 = dtype(o1)

    assert_eq(d3 - d2, d1)
    assert_eq(d3 - o2, o1)
    assert_eq((d3 - o2) - o1, {})
    ex(d3.__sub__, KeyError, {"g": 5})
    ex(d3.__sub__, KeyError, {"a": 20})

    assert_eq(d1, o1)
    assert_eq(d2, o2)
    assert_eq(d3, o3)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_multiply(dtype):
    o = {"a": 1, "b": 2, "c": 3}
    d = dtype(o)

    d.multiply({})
    assert_eq(d, {})
    d = dtype(o)

    d.multiply(o)
    assert_eq(d, {
        ("a", "a"): (1, 1), ("a", "b"): (1, 2), ("a", "c"): (1, 3),
        ("b", "a"): (2, 1), ("b", "b"): (2, 2), ("b", "c"): (2, 3),
        ("c", "a"): (3, 1), ("c", "b"): (3, 2), ("c", "c"): (3, 3)
    })
    d = dtype(o)
    d.multiply(o, lambda e1, e2: e1)
    assert_eq(d, o)
    d.multiply(o, lambda e1, e2: (e1.id + e2.id, (e1.value, e2.value)))
    assert_eq(d, {
        "aa": (1, 1), "ab": (1, 2), "ac": (1, 3),
        "ba": (2, 1), "bb": (2, 2), "bc": (2, 3),
        "ca": (3, 1), "cb": (3, 2), "cc": (3, 3)
    })


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___mul__(dtype):
    o = {"a": 1, "b": 2, "c": 3}
    d = dtype(o)

    assert_eq(d * {}, {})
    assert_eq(d, o)

    assert_eq(d * o, {
        ("a", "a"): (1, 1), ("a", "b"): (1, 2), ("a", "c"): (1, 3),
        ("b", "a"): (2, 1), ("b", "b"): (2, 2), ("b", "c"): (2, 3),
        ("c", "a"): (3, 1), ("c", "b"): (3, 2), ("c", "c"): (3, 3)
    })


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable_divide(dtype):
    o = {
        ("a", "a"): (1, 1), ("a", "b"): (1, 2), ("a", "c"): (1, 3),
        ("b", "a"): (2, 1), ("b", "b"): (2, 2), ("b", "c"): (2, 3),
        ("c", "a"): (3, 1), ("c", "b"): (3, 2), ("c", "c"): (3, 3)
    }
    o2 = {"a": 1, "b": 2, "c": 3}
    d = dtype(o)
    d.divide(o, lambda el, e2: (el.id[0], el.value[0]))
    assert_eq(d, o2)

    d.multiply(o2)
    assert_eq(d, o)
    d.divide(o2)
    assert_eq(d, o2)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___truediv__(dtype):
    o = {
        ("a", "a"): (1, 1), ("a", "b"): (1, 2), ("a", "c"): (1, 3),
        ("b", "a"): (2, 1), ("b", "b"): (2, 2), ("b", "c"): (2, 3),
        ("c", "a"): (3, 1), ("c", "b"): (3, 2), ("c", "c"): (3, 3)
    }
    o2 = {"a": 1, "b": 2, "c": 3}
    d = dtype(o2)
    assert_eq(d * d, o)
    # Python 2 doesn't have a / ? wtf?
    if not six.PY2:
        assert_eq((d * d) / d, d)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___le__(dtype):
    ao = {0: 0, 1: 1}
    bo = {2: 2, 3: 3}

    ad = dtype(ao)
    bd = dtype(bo)

    assert_op(ad, bd, operator.le)
    assert_eq(ad, ao)
    assert_eq(bd, bo)

    assert_op(ad, ad, operator.le)
    assert_op(bd, bd, operator.le)
    assert_eq(ad, ao)
    assert_eq(bd, bo)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___lt__(dtype):
    ao = {0: 0, 1: 1}
    bo = {2: 2, 3: 3}

    ad = dtype(ao)
    bd = dtype(bo)

    assert_op(ad, bd, operator.lt)
    assert_nop(bd, ad, operator.lt)
    assert_eq(ad, ao)
    assert_eq(bd, bo)

    assert_nop(ad, ad, operator.lt)
    assert_nop(bd, bd, operator.lt)
    assert_eq(ad, ao)
    assert_eq(bd, bo)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___ge__(dtype):
    ao = {0: 0, 1: 1}
    bo = {2: 2, 3: 3}

    ad = dtype(ao)
    bd = dtype(bo)

    assert_op(bd, ad, operator.ge)
    assert_nop(ad, bd, operator.ge)
    assert_eq(ad, ao)
    assert_eq(bd, bo)

    assert_op(ad, ad, operator.ge)
    assert_op(bd, bd, operator.ge)
    assert_eq(ad, ao)
    assert_eq(bd, bo)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_iterable___gt__(dtype):
    ao = {0: 0, 1: 1}
    bo = {2: 2, 3: 3}

    ad = dtype(ao)
    bd = dtype(bo)

    assert_op(bd, ad, operator.gt)
    assert_nop(ad, bd, operator.gt)
    assert_eq(ad, ao)
    assert_eq(bd, bo)

    assert_nop(ad, ad, operator.gt)
    assert_nop(bd, bd, operator.gt)
    assert_eq(ad, ao)
    assert_eq(bd, bo)


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


@pytest.mark.parametrize("dtype", unordered_dict_types)
def test_dictplus___eq__(dtype):
    d = dtype()
    d.insert(0, (0, "asdf"))
    d.insert(1, (1, "fdsa"))

    d2 = dtype()
    d2.insert(0, (1, "fdsa"))
    d2.insert(1, (0, "asdf"))

    assert_neq(d, 8)
    assert_neq(d2, 8)
    assert_eq(d, {1: "fdsa", 0: "asdf"})
    assert_eq(d2, {1: "fdsa", 0: "asdf"})
    assert_eq(d, d2)
    assert_eq(dtype(), {})
    assert_neq(dtype(), [])

    d3 = OrderedDictPlus()  # Have to insert manually for py2 dict compatiblilty
    d3[1] = "fdsa"
    d3[0] = "asdf"

    assert_eq(d, d3)  # DictPlus doesn't care about order
    assert_neq(d3, d)  # OrderedDictPlus does

    d4 = OrderedDictPlus()
    d4.insert(0, (0, "asdf"))
    d4.insert(1, (1, "fdsa"))
    assert_eq(d, d4)
    assert_eq(d4, d)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_dictplus_fromkeys(dtype):
    assert_eq(dict.fromkeys(["a", "b", "c"]), dtype.fromkeys(["a", "b", "c"]))
    assert_eq(dict.fromkeys(["a", "b", "c"], 10), dtype.fromkeys(["a", "b", "c"], 10))


@pytest.mark.parametrize("dtype", all_dict_types)
@pytest.mark.parametrize("data", [OrderedDictPlus(), {}, {"a": 1, "b": 2}])
def test_ordereddictplus___init__(dtype, data):
    assert_neq(dtype(), [])
    assert_eq(dtype(), {})
    assert_eq(dtype([]), {})
    assert_eq(dtype({}), {})
    assert_eq(dtype(dtype()), {})
    assert_eq(dtype([("a", 1), ("b", 2)]), {"a": 1, "b": 2})
    # subtest_ordereddictplus__init__(OrderedDictPlus())
    # subtest_ordereddictplus__init__({})
    # subtest_ordereddictplus__init__({"a": 1, "b": 2})

    d = dtype(data=data)
    assert_eq(d, data)
    assert_eq(dtype(data={"v": data}), {"v": data})


@pytest.mark.parametrize("dtype", ordered_dict_types)
def test_ordereddictplus___eq__(dtype):
    d = dtype()

    d.insert(0, (0, "asdf"))
    d.insert(1, (1, "fdsa"))

    d2 = dtype()
    d2.insert(0, (1, "fdsa"))
    d2.insert(1, (0, "asdf"))

    assert_neq(d, 8)
    assert_eq(d, {1: "fdsa", 0: "asdf"})
    assert_eq(d2, {1: "fdsa", 0: "asdf"})
    assert_neq(d, d2)
    assert_eq(dtype(), {})
    assert_neq(dtype(), [])

    d3 = DictPlus({1: "fdsa", 0: "asdf"})
    # assert_neq(d, d3)  # Removed this test because py2 dicts are ordered differently
    assert_eq(d3, d)


def test_functionallyinsensitivedictplus___init__():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus()
    d = FunctionallyInsensitiveDictPlus(compare_func=comp_func)
    d["a"] = 5
    assert_eq(d["a"], d["1a"])


def test_functionallyinsensitivedictplus__find_base_key():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(compare_func=comp_func)
    d["a"] = 5
    assert_eq(d._find_base_key("1a"), "a")


def test_functionallyinsensitivedictplus_getitem():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(compare_func=comp_func)
    d["a"] = 5
    assert_eq(d.getitem("a"), d.getitem("1a"))
    ex(d.getitem, KeyError, "asdf")


def test_functionallyinsensitivedictplus_pop():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(compare_func=comp_func)
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

    d = FunctionallyInsensitiveDictPlus(compare_func=comp_func)
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

    d = FunctionallyInsensitiveDictPlus(compare_func=comp_func)
    d["a"] = 5
    assert_eq(d.indexof("1a"), d.indexof("a"))


def test_functionallyinsensitivedictplus_setdefault():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(compare_func=comp_func)
    d["a"] = 5
    assert_eq(d.setdefault("1a"), ("a", 5))
    assert_eq(d.setdefault("b", 2), 2)


def test_functionallyinsensitivedictplus___contains__():
    def comp_func(new_key, old_key):
        if new_key == "1" + old_key or new_key == old_key:
            return True
        else:
            return False

    d = FunctionallyInsensitiveDictPlus(compare_func=comp_func)
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

    d = FunctionallyInsensitiveDictPlus(compare_func=comp_func)
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
    d = PrefixInsensitiveDictPlus(prefix_list=["http://", "https://"])
    d["google.com"] = 5
    assert_eq(d["http://google.com"], 5)
    assert_eq(d["https://google.com"], 5)

    d["http://google.com"] = 4
    assert_eq(d["google.com"], 4)
    assert_eq(d["https://google.com"], 4)


def test_suffixinsensitivedictplus___init__():
    d = SuffixInsensitiveDictPlus(suffix_list=[".com", ".net"])
    d["google"] = 5
    assert_eq(d["google.net"], 5)
    assert_eq(d["google.com"], 5)

    d["google.net"] = 4
    assert_eq(d["google"], 4)
    assert_eq(d["google.com"], 4)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_isinstance(dtype):
    d = dtype()
    assert isinstance(d, dict)


@pytest.mark.parametrize("dtype", all_dict_types)
def test_subdict_type(dtype):
    data = {"a": 1, "b": {"c": 2}}
    d = dtype(data)
    assert type(d["b"]) == type(d)