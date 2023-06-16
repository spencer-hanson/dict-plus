from dict_plus.utils import SimpleFlattener

data1 = {
    "input": {
        "a": {
            "aa1": 1,
            "aa2": 2,
            "aa3": 3
        },
        "b": 5
    },
    "expected": {
        "a_aa1": 1,
        "a_aa2": 2,
        "a_aa3": 3,
        "b": 5
    }
}

class DummyClass(object):
    pass

DUMMY = DummyClass()

data2 = {
    "input": {
        "a": {
            "b": DUMMY
        }
    },
    "expected": {
        "a/b": DUMMY
    }
}


def test_simpleflatten():
    r = SimpleFlattener().flatten(data1["input"])
    r2 = SimpleFlattener(simple_types=[DummyClass], delimiter="/").flatten(data2["input"])
    assert r == data1["expected"]
    assert r2 == data2["expected"]

# test_simpleflatten()