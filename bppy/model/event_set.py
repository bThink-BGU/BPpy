from bppy.model.b_event import BEvent
from inspect import signature


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
        super().__init__(lambda e: any([EventSetList.item_contains(item, e) for item in self.lst]))

    @staticmethod
    def item_contains(item, event):
        if isinstance(item, BEvent):
            return event == item
        elif len(signature(item.predicate).parameters) > 1:
            return item.predicate(event, item.data)
        else:
            return item.predicate(event)

