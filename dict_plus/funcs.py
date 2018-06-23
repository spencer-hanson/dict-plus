import functools


class Functions(object):
    @staticmethod
    def AND(*els):
        for el in els:
            if not el.value:
                return False, False
        return True, True

    @staticmethod
    def OR(*els):
        for el in els:
            if el:
                return True
        return False

    @staticmethod
    def LE(v1, v2):
        if v1 <= v2:
            return True
        else:
            return False

    @staticmethod
    def LT(v1, v2):
        if v1 < v2:
            return True
        else:
            return False

    @staticmethod
    def GE(v1, v2):
        if v1 >= v2:
            return True
        else:
            return False

    @staticmethod
    def GT(v1, v2):
        if v1 > v2:
            return True
        else:
            return False
