from dict_plus.dictplus import *
from dict_plus import *
from dict_plus.exceptions import *


def ex(f, ex_class, *args):
    try:
        f(*args)
    except Exception as _e:
        assert _e.__class__ == ex_class
    else:
        assert 8 != 8


##################


def test_keyvaluepair_parse_object():
    def subtest_keyvaluepair_parse_object(_id, val):
        parse = KeyValuePair.parse_object

        ex(parse, InvalidElementTypeException, (_id, _id, _id))
        ex(parse, InvalidElementTypeException, (val, val, val))

        assert parse((_id, val)) == (_id, val)
        assert parse((val, _id)) == (val, _id)

        assert parse(KeyValuePair(_id, val)) == (_id, val)
        assert parse(KeyValuePair(val, _id)) == (val, _id)
    subtest_keyvaluepair_parse_object("a", "b")
    subtest_keyvaluepair_parse_object("a", 1)
    subtest_keyvaluepair_parse_object(1, 1)


def test_keyvaluepair___eq__():
    assert KeyValuePair("a", "b") == {"a": "b"}


##################


def test_element___init__():
    ex(Element, TypeError, "id", None)
    ex(Element, TypeError, None, "value")
    assert KeyValuePair(0, 1) == KeyValuePair(obj=(0, 1))
    assert KeyValuePair(obj=KeyValuePair(0, 1)) == KeyValuePair(obj=(0, 1))


def test_element_parts():
    assert Element(0, 1) == (0, 1)


def test_element___eq__():
    d = OrderedDictPlus()
    d.insert(0, ("4", "3"))
    assert d.getitem("4") == KeyValuePair("4", "3")
    assert ("4", "3") == KeyValuePair("4", "3")
    assert KeyValuePair("a", "b") == KeyValuePair("a", "b")
    assert KeyValuePair("1", "2") == ("1", "2")
    assert KeyValuePair("1", "2") != ["1", "2"]
    assert KeyValuePair("a", "b") == {"a": "b"}
    assert KeyValuePair("c", "d") != {"a": "b", "c": "d"}


##################

def test_iterable_get():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    assert d.get("1") == "2"


def test_iterable_getitem():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    assert d.getitem("1") != 8
    assert d.getitem("1") == KeyValuePair("1", "2")


def test_iterable_insert():
    d = DictPlus()
    assert d.insert(12345, ("a", "g"))
    ex(d.insert, KeyError, 12345, ("a", "b"))
    assert d._indexes["a"] == 0
    assert d._elements[0] == ("a", "g")


def test_iterable_pop():
    d = DictPlus({"a": "b", "c": "d"})
    assert d.pop("a") == "b"
    assert d == {"c": "d"}


def test_iterable_popitem():
    d = DictPlus({"a": "b"})
    t = d.popitem()
    assert t == ("a", "b")
    ex(d.popitem, KeyError)


def test_iterable_copy():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    c = d.copy()
    assert d == c
    d.insert(-1, ("[E}", "no u"))
    assert d != c


def test_iterable_atindex():
    d = DictPlus({"a": 1, "b": 2})
    assert d.atindex(0) == ("a", 1)
    assert d.atindex(1) == ("b", 2)


def test_iterable___getitem__():
    d = OrderedDictPlus()
    d.insert(0, ("1", "2"))
    assert d.get("1") == d["1"]
    assert d["1"] == "2"
    # assert "1" in d
    # assert "5" not in d  # TODO: Fix 'in' bug
    ex(d.__getitem__, KeyError, "5")


def test_iterable___setitem__():
    d = OrderedDictPlus()
    d.insert(0, ("AAA", "AAA"))
    d["asdf"] = "ghjkl;"
    assert d == {"asdf": "ghjkl;", "AAA": "AAA"}
    d["asdf"] = "asdf"
    assert d == {"asdf": "asdf", "AAA": "AAA"}


def test_iterable___len__():
    assert len(DictPlus()) == 0
    assert len(DictPlus(a="b")) == 1
    d = DictPlus(a="1", b="2")
    assert len(d) == 2
    d.popitem()
    assert len(d) == 1
    d.insert(0, ("c", 3))
    assert len(d) == 2


def test_iterable___str__():
    assert str(DictPlus()) == str({})
    assert str(DictPlus({"a": "b"})) == str({"a": "b"})


def test_iterable_fromkeys():
    ex(Iterable.fromkeys, NotImplementedError, ["a"], 5)


def test_iterable_items():
    d = DictPlus()
    assert d.items() == {}.items()
    d.insert(0, ("a", "b"))
    assert d.items() == {"a": "b"}.items()


def test_iterable_keys():
    d = DictPlus()
    assert d.keys() == {}.keys()
    d.insert(0, ("a", 1))
    d.insert(1, ("b", 2))
    assert d.keys() == {"a": 1, "b": 2}.keys()


def test_iterable_values():
    d = DictPlus()
    assert d.values() == list({}.values())
    d.insert(0, ("a", 1))
    d.insert(1, ("b", 2))
    assert d.values() == list({"a": 1, "b": 2}.values())


def test_iterable_setdefault():
    d = DictPlus()
    d2 = {}
    assert d.setdefault("a", 1) == d2.setdefault("a", 1)
    assert d == d2
    assert d.setdefault("b") == d2.setdefault("b")
    assert d == d2


def test_iterable_todict():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    assert d.todict() == {"1": "2"}
    assert d == d.todict()
    assert d == d.copy().todict()


def test_iterable_swap():
    d = DictPlus({"a": {"aa": 1}, "b": {"bb": 2}})
    d.swap("a", "b")
    assert d.get("a") == {"bb": 2}
    assert d.get("b") == {"aa": 1}


def test_iterable_clear():
    d = DictPlus({"a": 1})
    assert d == {"a": 1}
    d.clear()
    assert d == {}


def test_iterable_update():
    def subtest_iterable_update(e, **kwargs):
        d = OrderedDictPlus()
        d.insert(0, ("1", "2"))
        d.update(e, **kwargs)
        assert d == {"1": "2", **dict(e), **kwargs}
        d.update({"1": "asdf"})
        assert d == {"1": "asdf", **dict(e), **kwargs}
        assert d.keys() == set(["1"] + list(dict(e).keys()) + list(kwargs.keys()))
        assert d.values() == ["asdf"] + list(dict(e).values()) + list(kwargs.values())

    subtest_iterable_update({"21": "12", "Y": "YZ"})
    subtest_iterable_update([("21", "12"), ("Y", "YZ")])
    subtest_iterable_update({"21": "12", "Y": "YZ"}, a="meow", b="cat")
    subtest_iterable_update([("21", "12"), ("Y", "YZ")], a="meow", b="cat")


def test_iterable_unupdate():
    def subtest_iterable_unupdate(e, ee, **kwargs):
        d = OrderedDictPlus()
        d.insert(0, ("1", "2"))
        d.update(e, **kwargs)
        assert d == {"1": "2", **dict(e), **kwargs}
        d.unupdate(e, **kwargs)
        assert d == {"1": "2"}

        try:
            d.unupdate(e, **kwargs)
        except Exception as ex:
            assert ex.__class__ == KeyError
        else:
            assert False

        d.update(e, **kwargs)
        try:
            d.unupdate(ee, **kwargs)
        except Exception as ex:
            assert ex.__class__ == InvalidElementValueException
        else:
            assert False

    subtest_iterable_unupdate({"gg": "ez"}, {"gg": "wp"}, a="meow", b="cat")
    subtest_iterable_unupdate({"gg": "ez"}, {"gg": "wp"})
    subtest_iterable_unupdate([("gg", "ez")], [("gg", "wp")], a="meow", b="cat")
    subtest_iterable_unupdate([("gg", "ez")], [("gg", "wp")])
    try:
        d = OrderedDictPlus()
        d.insert(0, ("1", "2"))
        d.insert(-1, ("A", "B"))
        d.unupdate(("A", "B"))
    except Exception as ex:
        assert ex.__class__ == ValueError
    else:
        assert False


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
    assert d == {"aa": 2, "ba": 4, "ca": 6}
    assert d.get("aa") == 2
    d.map(invfunc_e2e)
    assert d == od
    assert d.get("a") == 1


def test_iterable_rekey():
    def func_k2k(k):
        return k + "a"

    def invfunc_k2k(k):
        return k[:-1]
    o = {"a": 1, "b": 2}
    d = DictPlus(o)
    d.rekey(func_k2k)
    assert d == {"aa": 1, "ba": 2}
    assert d.get("aa") == 1
    d.rekey(invfunc_k2k)
    assert d.get("a") == 1
    assert d == o


def test_iterable_plus():
    o1 = {"a": 1, "b": 2}
    o2 = {"c": 3, "d": 4}
    o3 = {"a": 1, "b": 2, "c": 3, "d": 4}
    d1 = DictPlus(o1)
    d2 = DictPlus(o2)
    d3 = DictPlus(o3)

    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    assert d1.plus(d2) == d3
    assert d1 == d3
    d1 = DictPlus(o1)
    t = d1.plus(d2, func_ee2e)
    assert t == {"ac": 4, "bd": 6}
    d1 = DictPlus(o1)
    d1.insert(-1, ("g", 6))
    assert d1.plus(d2, func_ee2e) == {"ac": 4, "bd": 6, "g": 6}


def test_iterable_minus():
    raise NotImplementedError


def test_iterable_chop():
    raise NotImplementedError


def test_iterable_squish():
    raise NotImplementedError


def test_iterable_expand():
    raise NotImplementedError


def test_iterable_funcmap():
    raise NotImplementedError


def subtest_iterable_fold(fold_func):
    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    def func2_ee2e(*es):
        return KeyValuePair(es[0].id + es[1].id, es[0].value + es[1].value)

    def subsubtest_iterable_fold(di):
        g = getattr(di, fold_func)(func_ee2e)
        gp = getattr(di, fold_func)(func2_ee2e)
        assert gp == g
        return g

    d = DictPlus()
    assert subsubtest_iterable_fold(d) == {}
    d.insert(0, (1, 1))
    assert subsubtest_iterable_fold(d) == {1: 1}
    d.insert(1, (2, 2))
    assert subsubtest_iterable_fold(d) == {3: 3}


def test_iterable_fold_left():
    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    subtest_iterable_fold("fold_left")
    d = DictPlus()
    d.update([(0, "a"), (1, "b"), (2, "c")])
    r = d.fold_left(func_ee2e)
    assert r != d.fold_right(func_ee2e)
    assert r == {3: "abc"}


def test_iterable_fold_right():
    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    subtest_iterable_fold("fold_right")
    d = DictPlus()
    d.update([(0, "a"), (1, "b"), (2, "c")])
    r = d.fold_right(func_ee2e)
    assert r == {3: "cba"}


def test_iterable_multiply():
    raise NotImplementedError


def test_iterable_divide():
    raise NotImplementedError


def test_iterable___le__():
    raise NotImplementedError


def test_iterable___lt__():
    raise NotImplementedError


def test_iterable___ge__():
    raise NotImplementedError


def test_iterable___gt__():
    raise NotImplementedError


def test_iterable___add__():
    o1 = {"a": 1, "b": 2}
    o2 = {"c": 3, "d": 4}

    o3 = o1.copy()
    o3.update(o2)

    d1 = DictPlus(o1)
    d2 = DictPlus(o2)
    d3 = d1 + d2

    assert d1 + d3 == d3
    assert d1 + d2 == o3
    assert d1 + o2 == o3
    assert d2 + o1 == o3


def test_iterable___sub__():
    o1 = {"a": 1, "b": 2}
    o2 = {"c": 3, "d": 4}

    o3 = o1.copy()
    o3.update(o2)

    d3 = DictPlus(o3)
    d2 = DictPlus(o2)
    d1 = DictPlus(o1)

    assert d3 - d2 == d1
    assert d3 - o2 == o1
    assert d3 - o2 - o1 == {}
    ex(d3.__sub__, KeyError, {"g": 5})
    ex(d3.__sub__, KeyError, {"a": 20})

    assert d1 == o1
    assert d2 == o2
    assert d3 == o3

##################


def test_orderediterable_insert():
    d = OrderedDictPlus()
    assert d.insert(0, ("a", "b")) == KeyValuePair("a", "b")
    assert d.insert(1, ("b", "c")) == ("b", "c")
    assert d.insert(5, KeyValuePair("g", "h")) == KeyValuePair("g", "h")
    assert d.insert(0, KeyValuePair("e", "f")) == ("e", "f")
    assert d == {"a": "b", "b": "c", "g": "h", "e": "f"}
    assert d.values() == ["f", "b", "c", "h"]
    assert d.keys() == ["e", "a", "b", "g"]
    ex(d.insert, InvalidElementTypeException, 0, "meow")


def test_orderediterable_pop():
    d = OrderedDictPlus()
    d.insert(0, ("1", "2"))
    assert d.pop("1") == "2"
    assert d.pop("1", "2") == "2"


#################


def test_dictplus___eq__():
    d = DictPlus()
    d.insert(0, (0, "asdf"))
    d.insert(1, (1, "fdsa"))

    d2 = DictPlus()
    d2.insert(0, (1, "fdsa"))
    d2.insert(1, (0, "asdf"))

    assert d != 8
    assert d2 != 8
    assert d == {1: "fdsa", 0: "asdf"}
    assert d2 == {1: "fdsa", 0: "asdf"}
    assert d == d2
    assert DictPlus() == {}
    assert DictPlus() != []

    d3 = OrderedDictPlus({1: "fdsa", 0: "asdf"})
    assert d == d3
    assert d3 != d

    d4 = OrderedDictPlus()
    d4.insert(0, (0, "asdf"))
    d4.insert(1, (1, "fdsa"))
    assert d == d4
    assert d4 == d


def test_dictplus_fromkeys():
    assert dict.fromkeys(["a", "b", "c"]) == DictPlus.fromkeys(["a", "b", "c"])
    assert dict.fromkeys(["a", "b", "c"], 10) == DictPlus.fromkeys(["a", "b", "c"], 10)


##################


def test_ordereddictplus___init__():
    def subtest_ordereddictplus__init__(data):
        d = OrderedDictPlus(data=data)
        assert d == data
        assert OrderedDictPlus(data={"v": data}) == {"v": data}

    assert OrderedDictPlus() != []
    assert OrderedDictPlus() == {}
    subtest_ordereddictplus__init__({})
    subtest_ordereddictplus__init__({"a": 1, "b": 2})


def test_ordereddictplus___eq__():
    d = OrderedDictPlus()

    d.insert(0, (0, "asdf"))
    d.insert(1, (1, "fdsa"))

    d2 = OrderedDictPlus()
    d2.insert(0, (1, "fdsa"))
    d2.insert(1, (0, "asdf"))

    assert d != 8
    assert d == {1: "fdsa", 0: "asdf"}
    assert d2 == {1: "fdsa", 0: "asdf"}
    assert d != d2
    assert OrderedDictPlus() == {}
    assert OrderedDictPlus() != []

    d3 = DictPlus({1: "fdsa", 0: "asdf"})
    assert d != d3
    assert d3 == d


def test_ordereddictplus_fromkeys():
    assert dict.fromkeys(["a", "b", "c"]) == DictPlus.fromkeys(["a", "b", "c"])
    assert dict.fromkeys(["a", "b", "c"], 10) == DictPlus.fromkeys(["a", "b", "c"], 10)

# # .squish
# d = OrderedDictPlus()
# d.insert(0, ("1", "2"))
# d.insert(0, ("asdf", "[E]"))
#
# d.squish(["1", "asdf"], ["tt"], func2_ee2e)
# assert d == {"tt": "2[E]"}
# tw = 2


# KeyValuePair tests
tests = [
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
    test_iterable___setitem__,
    test_iterable___getitem__,
    test_iterable___len__,
    test_iterable___str__,
    test_iterable_fromkeys,
    test_iterable_items,
    test_iterable_keys,
    test_iterable_values,
    test_iterable_setdefault,
    test_iterable_todict,
    test_iterable_swap,
    test_iterable_clear,
    test_iterable_update,
    test_iterable_unupdate,
    test_iterable_map,
    test_iterable_rekey,
    test_iterable_plus,
    test_iterable_minus,
    test_iterable_chop,
    test_iterable_squish,
    test_iterable_expand,
    test_iterable_funcmap,
    test_iterable_fold_left,
    test_iterable_fold_right,
    test_iterable_multiply,
    test_iterable_divide,
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
        raise e
    total_count = total_count + 1

for k, v in results.items():
    print("{}:\n{}\n".format(k, v))

print("Passed: {} Total: {} - {}%".format(pass_count, total_count, round((pass_count/total_count), 4)))
