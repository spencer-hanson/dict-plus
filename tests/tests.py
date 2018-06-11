from dict_plus.dictplus import DictPlus
from dict_plus import KeyValuePair
from dict_plus.exceptions import *


# Iterable.get
def test_iterable_get():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    assert d.get("1") == "2"


# Iterable.getitem
def test_iterable_getitem():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    assert d.getitem("1") != 8
    assert d.getitem("1") == KeyValuePair("1", "2")


# Iterable.insert
def test_iterable_insert():
    d = DictPlus()
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


# Iterable.__eq__
def test_iterable_eq():
    d = DictPlus()
    d.insert(0, (0, "asdf"))
    d.insert(1, (1, "fdsa"))
    assert d != 8
    assert d == {1: "fdsa", 0: "asdf"}
    assert d != ["asdf", "fdsa"]
    assert d != ["fdsa", "asdf"]
    assert d != ["2"]
    assert DictPlus() == {}
    assert DictPlus() != []


# Iterable.__copy__
def test_iterable_copy():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    c = d.copy()
    assert d == c
    d.insert(-1, ("[E}", "no u"))
    assert d != c


# Iterable.__getitem__
def test_iterable___getitem__():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    assert d.get("1") == d["1"]
    assert d["1"] == "2"


def test_iterable___setitem__():
    d = DictPlus()
    d.insert(0, ("AAA", "AAA"))
    d["asdf"] = "ghjkl;"
    assert d == {"asdf": "ghjkl;", "AAA": "AAA"}
    d["asdf"] = "asdf"
    assert d == {"asdf": "asdf", "AAA": "AAA"}


# Iterable.pop
def test_iterable_pop():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    assert d.pop("1") == "2"
    assert d.pop("1", "2") == "2"


# Iterable.update
def test_iterable_update():
    def subtest_iterable_update(e, **kwargs):
        d = DictPlus()
        d.insert(0, ("1", "2"))
        d.update(e, **kwargs)
        assert d == {"1": "2", **dict(e), **kwargs}
        d.update({"1": "asdf"})
        assert d == {"1": "asdf", **dict(e), **kwargs}
        assert d.keys() == list(dict(e).keys()) + list(kwargs.keys()) + ["1"]
        assert d.values() == list(dict(e).values()) + list(kwargs.values()) + ["asdf"]
        assert d.items() == list(zip(list(list(dict(e).keys()) + list(kwargs.keys()) + ["1"], dict(e).values()) + list(kwargs.values()) + ["asdf"]))
    subtest_iterable_update({"21": "12", "Y": "YZ"})
    subtest_iterable_update([("21", "12"), ("Y", "YZ")])
    subtest_iterable_update({"21": "12", "Y": "YZ"}, a="meow", b="cat")
    subtest_iterable_update([("21", "12"), ("Y", "YZ")], a="meow", b="cat")


def test_iterable_todict():
    d = DictPlus()
    d.insert(0, ("1", "2"))
    assert d == d.todict()
    assert d == d.copy().todict()


# Iterable.unupdate
def test_iterable_unupdate():
    def subtest_iterable_unupdate(e, ee, **kwargs):
        d = DictPlus()
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
        d = DictPlus()
        d.insert(0, ("1", "2"))
        d.insert(-1, ("A", "B"))
        d.unupdate(("A", "B"))
    except Exception as ex:
        assert ex.__class__ == ValueError
    else:
        assert False


# Iterator.map
def test_iterable_map():
    d = DictPlus()
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


# DictPlus.__init__
def test_dictplus___init__():
    def subtest_dictplus__init__(data):
        d = DictPlus(data=data)
        assert d == data
        assert DictPlus(data={"v": data}) == {"v": data}

    assert DictPlus() != []
    assert DictPlus() == {}
    # subtest_dictplus__init__([])
    subtest_dictplus__init__({})
    # TODO test for ListPlus
    # subtest_dictplus__init__([1, 2, 3])
    # subtest_dictplus__init__([KeyValuePair(0, 1), KeyValuePair(1, 2)])
    subtest_dictplus__init__({"a": 1, "b": 2})
    # subtest_dictplus__init__([1])


# Element.__eq__
def test_element_eq():
    d = DictPlus()
    d.insert(0, ("4", "3"))
    assert d.getitem("4") == KeyValuePair("4", "3")
    assert ("4", "3") == KeyValuePair("4", "3")
    assert KeyValuePair("a", "b") == KeyValuePair("a", "b")
    assert KeyValuePair("1", "2") == ("1", "2")
    assert KeyValuePair("1", "2") != ["1", "2"]
    assert KeyValuePair("a", "b") == {"a": "b"}
    assert KeyValuePair("c", "d") != {"a": "b", "c": "d"}


def func_ee2e(e1, e2):
    return e1.id + e2.id, e1.value + e2.value


def func2_ee2e(*es):
    return KeyValuePair(es[0].id + es[1].id, es[0].value + es[1].value)


# Iterator.fold_left
def subtest_iterable_fold(fold_func):
    def subsubtest_iterable_fold_left(di):
        g = getattr(di, fold_func)(func_ee2e)
        gp = getattr(di, fold_func)(func2_ee2e)
        assert gp == g
        return g

    d = DictPlus()
    assert subsubtest_iterable_fold_left(d) == {}
    d.insert(0, (1, 1))
    assert subsubtest_iterable_fold_left(d) == {1: 1}
    d.insert(1, (2, 2))
    assert subsubtest_iterable_fold_left(d) == {3: 3}


def test_iterable_fold_left():
    subtest_iterable_fold("fold_left")
    d = DictPlus()
    d.update([(0, "a"), (1, "b"), (2, "c")])
    r0 = d.fold_left(func_ee2e)
    r1 = d.fold_right(func_ee2e)
    assert r0 != r1
    assert r0 == {3: "abc"}
    assert r1 == {3: "bca"}


def test_iterable_fold_right():
    subtest_iterable_fold("fold_right")

#
# # .fold_right
# h = d.fold_right(func_ee2e)
# hp = d.fold_right(func2_ee2e)
# assert h == hp
#
# # .squish
# d = DictPlus()
# d.insert(0, ("1", "2"))
# d.insert(0, ("asdf", "[E]"))
#
# d.squish(["1", "asdf"], ["tt"], func2_ee2e)
# assert d == {"tt": "2[E]"}
# tw = 2


# DictPlus tests
test_dictplus___init__()

# KeyValuePair tests

# Element tests
test_element_eq()

# Iterable tests
test_iterable_get()
test_iterable_eq()
test_iterable_getitem()
test_iterable_insert()
test_iterable_pop()
test_iterable_copy()
test_iterable___setitem__()
test_iterable___getitem__()
test_iterable_update()
test_iterable_unupdate()

test_iterable_map()
test_iterable_fold_left()
test_iterable_fold_right()
