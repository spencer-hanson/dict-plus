class Functions(object):
    @staticmethod
    def AND(*els):
        """
        Basic AND function operation for elements

        Args:
            *els: Element-like instances to AND values with

        Returns:
            (True, True) if all values evaluate to true
            (False, False) otherwise

        """
        for el in els:
            if not el.value:
                return False, False
        return True, True

    @staticmethod
    def OR(*els):
        """
        Basic OR function operation for elements
        Args:
            *els: Element-like instances to OR values with

        Returns:
            True if any value evaluates to True

        """
        for el in els:
            if el:
                return True
        return False

    @staticmethod
    def LE(v1, v2):
        """
        Is v1 <= v2 ?
        Args:
            v1: Value 1
            v2: Value 2

        Returns:
            True if v1 <= v2 else false
        """
        if v1 <= v2:
            return True
        else:
            return False

    @staticmethod
    def LT(v1, v2):
        """
        Is v1 < v2 ?
        Args:
            v1: Value 1
            v2: Value 2

        Returns:
            True if v1 < v2 else false
        """
        if v1 < v2:
            return True
        else:
            return False

    @staticmethod
    def GE(v1, v2):
        """
        Is v1 >= v2 ?
        Args:
            v1: Value 1
            v2: Value 2

        Returns:
            True if v1 >= v2 else False
        """
        if v1 >= v2:
            return True
        else:
            return False

    @staticmethod
    def GT(v1, v2):
        """
        Is v1 > v2 ?
        Args:
            v1: Value 1
            v2: Value 2

        Returns:
            True if v1 .>v2 else false
        """
        if v1 > v2:
            return True
        else:
            return False
