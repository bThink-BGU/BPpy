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
    def __init__(self, name="", data={}, dist=None):
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
        return tuple([self.name]) + tuple(str(self.data.items())) + tuple([self.__dist_repr__])

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, BEvent) and self.__key() == other.__key()

    def __dist_repr__(self):
        dist_str = 'c'
        if self.dist:
            dist_str = str(self.dist.pdf.items())
        return dist_str

    def __repr__(self):
        return "{}(name={},data={},dist={})".format(self.__class__.__name__, self.name, self.data, self.__dist_repr__())

    def __str__(self):
        return self.__repr__()



