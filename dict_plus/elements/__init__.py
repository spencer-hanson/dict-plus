from dict_plus.elements.element import Element, KeyValuePair, ListElement


class ElementFactory(object):
    """
    Factory to create Elements within Dictionaries
    """

    @staticmethod
    def element(subclass_type, superclass_type):
        """Create a new element of type subclass_type in containing dictionary of type superclass_type

        Args:
            subclass_type: Type of Element to create, ie KeyValuePair
            superclass_type: Type of Dictionary to hold this element, ie. SortedDictPlus

        Returns:
            A new element type class for the specific use of the subclass type and superclass type

        """
        class ElementType(subclass_type):
            @staticmethod
            def get_dictlike_supertype():
                return superclass_type

        ElementType.__name__ = "[{dict_type}]{el_type}".format(
            dict_type=superclass_type.__name__,
            el_type=subclass_type.__name__
        )

        return ElementType

