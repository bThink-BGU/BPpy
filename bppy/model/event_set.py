from bppy.model.b_event import BEvent
from inspect import signature, getsource


class EventSet:
    """
    A class to represent a symbolically defined set of events using a given predicate.

    Attributes
    ----------
    predicate : callable
        The predicate that tests if an event is a member of this event set.
    data : dict
        Additional keyword arguments that could be used by the predicate.
    """

    def __init__(self, predicate, **kwargs):
        """
        Constructs all the necessary attributes for the EventSet object.

        Parameters
        ----------
        predicate : callable
            The predicate that tests if an event is a member of this event set. It should be a function
            that takes an event as its first argument and returns a boolean.
        **kwargs : dict
            Additional keyword arguments that could be used by the predicate.
        """
        self.predicate = predicate
        self.data = kwargs

    def __contains__(self, event):
        if len(signature(self.predicate).parameters) > 1:
            return self.predicate(event, self.data)
        else:
            return self.predicate(event)

    def __key(self):
        return str(getsource(self.predicate)) + str(self.data)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __str__(self):
        return self.__key()

    def __repr__(self):
        return self.__str__()


class All(EventSet):
    """
    A class to represent the set of all events.
    """
    def __init__(self):
        super().__init__(lambda e: True)


class EmptyEventSet(EventSet):
    """
    A class to represent an empty event set.
    """
    def __init__(self):
        super().__init__(lambda e: False)


class AllExcept(EventSet):
    """
    A class to represent a set of all events except some specified event or event set.
    """
    def __init__(self, event):
        """
        Constructs all the necessary attributes for the AllExcept object.

        If the input event is an instance of BEvent, an EventSet is created with a predicate that
        matches all events except for the input event. If the input event is an EventSet, an EventSet is
        created with a predicate that matches all events not contained in the input EventSet.

        Parameters
        ----------
        event : `BEvent <bppy.model.b_event.BEvent>` or `EventSet <bppy.model.event_set.EventSet>`
            The event or set of events to be excluded from the event set.
        """
        if isinstance(event, BEvent):
            super().__init__(lambda e: event != e)
        else:  # Event Set
            super().__init__(lambda e: not event.__contains__(e))


class EventSetList(EventSet):
    """
    A class to represent a union of event sets and events.
    """
    def __init__(self, lst):
        """
        Constructs all the necessary attributes for the EventSetList object.

        Parameters
        ----------
        lst : list
            A list of `BEvent <bppy.model.b_event.BEvent>` or `EventSet <bppy.model.event_set.EventSet>` objects.
            The resulting EventSetList will contain any event that is equal to a BEvent
            in the list or is contained in an EventSet in the list.
        """
        self.lst = lst
        super().__init__(lambda e: any([EventSetList._item_contains(item, e) for item in self.lst]))

    @staticmethod
    def _item_contains(item, event):
        if isinstance(item, BEvent):
            return event == item
        elif len(signature(item.predicate).parameters) > 1:
            return item.predicate(event, item.data)
        else:
            return item.predicate(event)

