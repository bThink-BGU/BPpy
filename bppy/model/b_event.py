class BEvent:
    """
    A class to represent a Behavioral Event (BEvent) object.

    Attributes
    ----------
    name : str
        The name of the event.
    data : dict
        Additional data associated with the event.
    """
    def __init__(self, name="", data={}):
        """
        Constructs all the necessary attributes for the BEvent object.

        Parameters
        ----------
        name : str
            The name of the event.
        data : dict
            Additional data associated with the event.
        """
        self.name = name
        self.data = data

    def __key(self):
        return tuple([self.name]) + tuple(str(self.data.items()))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, BEvent) and self.__key() == other.__key()

    def __repr__(self):
        return "{}(name={},data={})".format(self.__class__.__name__, self.name, self.data)

    def __str__(self):
        return self.__repr__()



