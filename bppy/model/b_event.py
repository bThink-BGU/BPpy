class BEvent:
    """
    A class to represent a Behavioral Event (BEvent) object.

    Attributes
    ----------
    name : str
        The name of the event.
    data : dict
        Additional data associated with the event.
    dist : Categorical
        A distribution object on possible, mutually exclusive events.
    """
    def __init__(self, name="", data={}, dist={}):
        """
        Constructs all the necessary attributes for the BEvent object.

        Parameters
        ----------
        name : str
            The name of the event.
        data : dict
            Additional data associated with the event.
        dist : Categorical
            A distribution object on possible, mutually exclusive events.
        """
        self.name = name
        self.data = data
        self.dist = dist

    def __key(self):
        return tuple([self.name]) + tuple(str(self.data.items())) + tuple(str(self.data.dist()))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, BEvent) and self.__key() == other.__key()

    def __repr__(self):
        return "{}(name={},data={},dist={})".format(self.__class__.__name__, self.name, self.data, self.dist)

    def __str__(self):
        return self.__repr__()



