from dict_plus.exceptions import *
from dict_plus.etypes import *


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


class Element(object):
    """Element superclass of an item in an Iterable
    Must have an id and value, where id is unique to the Element
    Subclasses can give other restrictions to what can and can't be used
    """

    def __init__(self, _id=None, value=None):
        """Create a new Element, must include either id and value or just id
        If just id is used, it will attempt to parse it into self.id and self.value
        Otherwise, self.id = id and self.value = value

        Args:
            _id: Id of Element, or object to be parsed
            value: Value of the element, required if _id isn't going to be parsed

        """
        if _id and not value:
            self.id, self.value = self.parse_object(_id)
        else:
            if _id is None or value is None:
                raise TypeError("Invalid args, must provide id and value or object")
            self.id = _id
            self.value = value

    @staticmethod
    def get_dictlike_supertype():
        """Get the type of the containing dictionary so that items within the dict are also of the same type
        By default will raise a NotImplemented error, so that it can be implemeneted during instantiation, by using
        ElementFactory.element()

        Examples:
            So we convert any dict-like values recursively using the typing of the superclass dictionary class type::

                >>>mydict = DictPlus({"a": DictPlus({"b": 1}), "c": {"d": 1}, ...})
                mydict["c"] == DictPlus({"d": 1})


        Returns:
            A Iterable classtype

        """
        raise NotImplementedError("No supertype defined in this Element! Use ElementFactory.element()")

    def parse_object(self, obj):
        """Parse an object into an Element type, possibly raising InvalidElementTypeException if the object cannot be
        parsed

        Args:
            obj: Element-like object to be parsed

        Raises:
            InvalidElementTypeException: If the object cannot be parsed

        Returns:
            parsed Element instance

        """
        raise NotImplementedError("Can't parse object as an Element!")

    def parts(self):
        """Break down the Element into a tuple, with (id, value)

        Returns
            Tuple like (id, value)

        """
        return self.id, self.value

    def __eq__(self, other):
        """Check if self == other
        Not implemented for Element

        Args:
            other: Element-like

        Returns
            True if equal or False if not

        """
        raise NotImplementedError("Can't equate superclass Element!")

    def __str__(self):
        """String representation of the Element

        Returns:
            String representing self

        """
        return "<{}, {}>".format(self.id, self.value)

    def copy(self):
        """Make a shallow copy of self

        Returns:
            Copied version of self

        """
        return self.__class__(self.id, self.value)


class KeyValuePair(Element):
    """
    General use Element implementation
    """

    def parse_object(self, obj):
        """
        Parse an object into a KeyValuePair

        Args:
            obj: Object to be parsed

        Returns:
            KeyValuePair instance

        """
        if isinstance(obj, KeyValuePair):
            return obj.id, obj.value
        if not isinstance(obj, (list, tuple)):
            raise InvalidElementTypeException("Invalid KeyPair object, must be a list, tuple or KeyValuePair!")
        if len(obj) != 2:
            raise InvalidElementTypeException("Invalid KeyPair object, length must be 2")

        key = obj[0]
        val = obj[1]
        if isinstance(val, DictType):
            val = self.get_dictlike_supertype()(val)

        if isinstance(val, ListType):
            for i in range(0, len(val)):
                if isinstance(val[i], DictType):
                    val[i] = self.get_dictlike_supertype()(val[i])

        return key, val

    @staticmethod
    def get_dictlike_supertype():
        """Get the type of the containing dictionary so that items within the dict are also of the same type
        By default will raise a NotImplemented error, so that it can be implemented during instantiation, by using
        ElementFactory.element()

        Examples:
            So we convert any dict-like values recursively using the typing of the superclass dictionary class type::
                >> mydict = DictPlus({"a": DictPlus({"b": 1}), "c": {"d": 1}, ...})
                mydict["c"] == DictPlus({"d": 1})

        Returns:
            Element Instance

        """
        raise NotImplementedError("No supertype defined in this Element! Use ElementFactory.element()")

    def __eq__(self, other):
        """Check if self == other
        if other is a KeyValuePair, other.id == self.id and self.value == other.value
        if other is a tuple, treat it as (id, value) and check for equality there

        Args:
            other: Element-like

        Returns:
            True or False

        """
        if isinstance(other, dict) and len(other) == 1:
            k, v = list(other.items())[0]
            if k == self.id and v == self.value:
                return True
        elif isinstance(other, KeyValuePair) and other.id == self.id and self.value == other.value:
            return True
        elif isinstance(other, tuple) and self.id == other[0] and self.value == other[1]:
            return True

    def __ne__(self, other):
        """Check if element is not equal,
        Args:
            other: Element-like to compare against

        Returns:
            True or False

        """
        return not self.__eq__(other)
