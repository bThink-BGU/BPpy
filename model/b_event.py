
class BEvent:

    def __init__(self, name="", data={}):
        self.name = name
        self.data = data

    def __key(self):
        return tuple([self.name]) + tuple(self.data.items())

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, BEvent) and self.__key() == other.__key()

    def __repr__(self):
        return "BEvent(name={},data={})".format(self.name, self.data)

    def __str__(self):
        return self.__repr__()

