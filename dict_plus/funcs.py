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
    def LE(e1, e2):
        if e1 <= e2:
            return True
        else:
            return False

    @staticmethod
    def LT(e1, e2):
        if e1 < e2:
            return True
        else:
            return False

    @staticmethod
    def GE(e1, e2):
        if e1 >= e2:
            return True
        else:
            return False

    @staticmethod
    def GT(e1, e2):
        if e1 > e2:
            return True
        else:
            return False
