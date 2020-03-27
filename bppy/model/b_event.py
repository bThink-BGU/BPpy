from inspect import signature


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
        return "{}(name={},data={})".format(self.__class__.__name__, self.name, self.data)

    def __str__(self):
        return self.__repr__()


class EventSet:

    def __init__(self, predicate, **kwargs):
        self.predicate = predicate
        self.data = kwargs

    def __contains__(self, event):
        if len(signature(self.predicate).parameters) > 1:
            return self.predicate(event, self.data)
        else:
            return self.predicate(event)


class All(EventSet):
    def __init__(self):
        super().__init__(lambda e: True)


class EmptyEventSet(EventSet):
    def __init__(self):
        super().__init__(lambda e: False)


class AllExcept(EventSet):
    def __init__(self, event):
        if isinstance(event, BEvent):
            super().__init__(lambda e: event != e)
        else:  # Event Set
            super().__init__(lambda e: not event.__contains__(e))


class EventSetList(EventSet):
    def __init__(self, lst):
        self.lst = lst

    def __contains__(self, event):
        return any([EventSetList.item_contains(item, event) for item in self.lst])

    @staticmethod
    def item_contains(item, event):
        if isinstance(item, BEvent):
            return event == item
        elif len(signature(item.predicate).parameters) > 1:
            return item.predicate(event, item.data)
        else:
            return item.predicate(event)


