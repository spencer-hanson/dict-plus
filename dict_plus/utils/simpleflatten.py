
class SimpleFlattener(object):
    """
    Utility class to flatten simple dictionaries into a top-level only dict
    e.g.
    {"a": {"a1": 1, "a2": 2}, "b": {"b1": 3, "b2": 4}}
    would flatten to
    {"a_a1": 1, "a_a2": 2, "b_b1": 3, "b_b2": 4}

    Another example:
    {"a": [{"a1": [1], "a2": [2]},{"a1": [3] "a2": [4,5], "a3": [5]}] }
    would flatten to
    {"a_a1": [[1],[3]], "a_a2": [[2],[4,5]], "a_a3": [None, [5]]}

    Not meant to be a general dictionary flattener

    """

    def __init__(self, simple_types=None):
        self.simple_types = {str, bytes, int, float, bool, tuple}
        for s in simple_types:
            self.simple_types.add(s)

        pass

    pass
