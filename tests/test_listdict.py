from dict_plus.lists import ListDict
from dict_plus import DictPlus


def test_all():
    data = [
        {"a": 1},
        {"a": 2},
        {"a": 3, "b": 5}
    ]

    data2 = [
        {"cat": 1, "bat": 2, "hat": 3, "car": 55},
        {"cat": 2, "bat": 3, "hat": 4, "car": 55, "bar": 6},
        {"cat": 3, "bat": 4, "hat": 5, "car": 55, "bar": 6},
        {"cat": 4, "bat": 5, "hat": 6, "bar": 6},
    ]
    ld = ListDict(data)


    def mapfunc(d):
        d["h"] = "i"
        return d


    def submapfunc(k, v):
        return k + "a", v


    ld.map(mapfunc)
    ld.submap(submapfunc)
    ld.inserteach(5, "a")
    ld.inserteach("a", 10, overwrite_exist=True)
    ld.append({"b": 4})
    ld.inserteach("a", 0, overwrite_exist=False)
    r1 = ld.popeach("a")
    r2 = ld.popeach("b", None)

    ld = ListDict(data)


    def popmapfunc(value):
        return "c", [1, 2, value]


    ld.popmap("a", popmapfunc)

    ld = ListDict(data2)
    r3 = ld.popregex(".at")

    ld = ListDict(data2)
    r4 = ld.popregex(".ar", nonexist_value="beans")

    ld = ListDict(data2)
    r5 = ld.aggregate()
    r6 = ld.aggregate("novalue")

    r7 = ld.hoist("car")
    r8 = ld.hoist_multiple(["car", "cat"])

    ld.aggregate(None).disaggregate()
    ld.aggregate().disaggregate()


    # TODO move this to other file
    data3 = {"cat": 2, "bat": 3, "hat": 4, "car": 55, "bar": 6}
    d = DictPlus(data3)

    r9 = d.rekey_regex("c")
    r10 = d.rekey_regex("c", "beans")

    r11 = d.pop_regex(".?at")

    tw = 2

