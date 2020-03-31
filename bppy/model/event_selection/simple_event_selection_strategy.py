from bppy.model.event_selection.event_selection_strategy import EventSelectionStrategy
from bppy.model.b_event import BEvent
from bppy.model.event_set import EmptyEventSet
import random
from collections.abc import Iterable


class SimpleEventSelectionStrategy(EventSelectionStrategy):

    def is_satisfied(self, event, statement):
        if isinstance(statement.get('request'), BEvent):
            if isinstance(statement.get('waitFor'), BEvent):
                return statement.get('request') == event or statement.get('waitFor') == event
            else:
                return statement.get('request') == event or statement.get('waitFor', EmptyEventSet()).__contains__(event)
        else:
            if isinstance(statement.get('waitFor'), BEvent):
                return statement.get('request', EmptyEventSet()).__contains__(event) or statement.get('waitFor') == event
            else:
                return statement.get('request', EmptyEventSet()).__contains__(event) or statement.get('waitFor', EmptyEventSet()).__contains__(event)

    def selectable_events(self, statements):
        possible_events = set()
        for statement in statements:
            if 'request' in statement:  # should be eligible for sets
                if isinstance(statement['request'], Iterable):
                    possible_events.update(statement['request'])
                elif isinstance(statement['request'], BEvent):
                    possible_events.add(statement['request'])
                else:
                    raise TypeError("request parameter should be BEvent or iterable")
        for statement in statements:
            if 'block' in statement:
                if isinstance(statement.get('block'), BEvent):
                    possible_events.discard(statement.get('block'))
                else:
                    possible_events = {x for x in possible_events if x not in statement.get('block')}
        return possible_events

    def select(self, statements):
        selectable_events = self.selectable_events(statements)
        if selectable_events:
            return random.choice(tuple(selectable_events))
        else:
            return None

