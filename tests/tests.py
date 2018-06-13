from dict_plus.dictplus import OrderedDictPlus
from dict_plus import KeyValuePair
from dict_plus.exceptions import *


##################


def test_keyvaluepair_parse_object():
    raise NotImplementedError


def test_keyvaluepair___eq__():
    raise NotImplementedError


##################


def test_element___init__():
    raise NotImplementedError


def test_element_parts():
    raise NotImplementedError


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
    d = OrderedDictPlus()
    d.insert(0, ("1", "2"))
    assert d.get("1") == "2"


def test_iterable_getitem():
    d = OrderedDictPlus()
    d.insert(0, ("1", "2"))
    assert d.getitem("1") != 8
    assert d.getitem("1") == KeyValuePair("1", "2")


def test_iterable_insert():
    raise NotImplementedError


def test_iterable_pop():
    raise NotImplementedError


def test_iterable_popitem():
    raise NotImplementedError


def test_iterable_copy():
    d = OrderedDictPlus()
    d.insert(0, ("1", "2"))
    c = d.copy()
    assert d == c
    d.insert(-1, ("[E}", "no u"))
    assert d != c


def test_iterable___getitem__():
    d = OrderedDictPlus()
    d.insert(0, ("1", "2"))
    assert d.get("1") == d["1"]
    assert d["1"] == "2"


def test_iterable___setitem__():
    d = OrderedDictPlus()
    d.insert(0, ("AAA", "AAA"))
    d["asdf"] = "ghjkl;"
    assert d == {"asdf": "ghjkl;", "AAA": "AAA"}
    d["asdf"] = "asdf"
    assert d == {"asdf": "asdf", "AAA": "AAA"}


def test_iterable___len__():
    raise NotImplementedError


def test_iterable___str__():
    raise NotImplementedError


def test_iterable_fromkeys():
    raise NotImplementedError


def test_iterable_items():
    raise NotImplementedError


def test_iterable_keys():
    raise NotImplementedError


def test_iterable_values():
    raise NotImplementedError


def test_iterable_setdefault():
    raise NotImplementedError


def test_iterable_todict():
    d = OrderedDictPlus()
    d.insert(0, ("1", "2"))
    assert d.todict() == {"1": "2"}
    assert d == d.todict()
    assert d == d.copy().todict()


def test_iterable_swap():
    raise NotImplementedError


def test_iterable_clear():
    raise NotImplementedError


def test_iterable_update():
    def subtest_iterable_update(e, **kwargs):
        d = OrderedDictPlus()
        d.insert(0, ("1", "2"))
        d.update(e, **kwargs)
        assert d == {"1": "2", **dict(e), **kwargs}
        d.update({"1": "asdf"})
        assert d == {"1": "asdf", **dict(e), **kwargs}
        assert d.keys() == ["1"] + list(dict(e).keys()) + list(kwargs.keys())
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

    def func_e2e(e):
        k, v = e.parts()
        return str(k) + "a", v * 2

    def invfunc_e2e(e):
        k, v = e.parts()
        return str(k)[:-1], v / 2

    od = d.copy()
    d.map(func_e2e)
    assert d == {"aa": 2, "ba": 4, "ca": 6}
    d.map(invfunc_e2e)
    assert d == od


def test_iterable_rekey():
    raise NotImplementedError


def test_iterable_plus():
    raise NotImplementedError


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


##################


def subtest_orderediterable_fold(fold_func):
    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    def func2_ee2e(*es):
        return KeyValuePair(es[0].id + es[1].id, es[0].value + es[1].value)

    def subsubtest_iterable_fold_left(di):
        g = getattr(di, fold_func)(func_ee2e)
        gp = getattr(di, fold_func)(func2_ee2e)
        assert gp == g
        return g

    d = OrderedDictPlus()
    assert subsubtest_iterable_fold_left(d) == {}
    d.insert(0, (1, 1))
    assert subsubtest_iterable_fold_left(d) == {1: 1}
    d.insert(1, (2, 2))
    assert subsubtest_iterable_fold_left(d) == {3: 3}


def test_orderediterable_fold_left():
    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    subtest_orderediterable_fold("fold_left")
    d = OrderedDictPlus()
    d.update([(0, "a"), (1, "b"), (2, "c")])
    r = d.fold_left(func_ee2e)
    assert r != d.fold_right(func_ee2e)
    assert r == {3: "abc"}


def test_orderediterable_fold_right():
    def func_ee2e(e1, e2):
        return e1.id + e2.id, e1.value + e2.value

    subtest_orderediterable_fold("fold_right")
    d = OrderedDictPlus()
    d.update([(0, "a"), (1, "b"), (2, "c")])
    r = d.fold_right(func_ee2e)
    assert r == {3: "cba"}


def test_orderediterable_insert():
    d = OrderedDictPlus()
    assert d.insert(0, ("a", "b")) == KeyValuePair("a", "b")
    assert d.insert(1, ("b", "c")) == ("b", "c")
    assert d.insert(5, KeyValuePair("g", "h")) == KeyValuePair("g", "h")
    assert d.insert(0, KeyValuePair("e", "f")) == ("e", "f")
    assert d == {"a": "b", "b": "c", "g": "h", "e": "f"}
    assert d.values() == ["f", "b", "c", "h"]
    assert d.keys() == ["e", "a", "b", "g"]
    try:
        d.insert(0, "meow")
    except Exception as e:
        assert e.__class__ == InvalidElementTypeException
    else:
        assert 2 != 2  # Throw assertion error since exception wasn't thrown


def test_orderediterable_pop():
    d = OrderedDictPlus()
    d.insert(0, ("1", "2"))
    assert d.pop("1") == "2"
    assert d.pop("1", "2") == "2"


def test_orderediterable_multiply():
    raise NotImplementedError


def test_orderediterable_divide():
    raise NotImplementedError


def test_orderediterable___le__():
    raise NotImplementedError


def test_orderediterable___lt__():
    raise NotImplementedError

def test_orderediterable___ge__():
    raise NotImplementedError


def test_orderediterable___gt__():
    raise NotImplementedError


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
    assert d != 8
    assert d == {1: "fdsa", 0: "asdf"}
    assert d != ["asdf", "fdsa"]
    assert d != ["fdsa", "asdf"]
    assert d != ["2"]
    assert OrderedDictPlus() == {}
    assert OrderedDictPlus() != []


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

    # OrderedIterable tests
    test_orderediterable_fold_left,
    test_orderediterable_fold_right,
    test_orderediterable_insert,
    test_orderediterable_pop,
    test_orderediterable_multiply,
    test_orderediterable_divide,
    test_orderediterable___le__,
    test_orderediterable___lt__,
    test_orderediterable___ge__,
    test_orderediterable___gt__,

    # DictPlus tests

    # OrderedDictPlus tests
    test_ordereddictplus___init__,
    test_ordereddictplus___eq__]

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
        results[name] = "{}: \'{}\'".format(e.__class__.__name__, str(e))
    total_count = total_count + 1

for k, v in results.items():
    print("{}:\n{}\n".format(k, v))

print("Passed: {} Total: {} -- {}%".format(pass_count, total_count, round((pass_count/total_count), 4)))
