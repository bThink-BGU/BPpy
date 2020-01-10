from model.event_selection.event_selection_strategy import EventSelectionStrategy
import random
from model.b_event import BEvent, EmptyEventSet


class SimpleEventSelectionStrategy(EventSelectionStrategy):

    def is_satisfied(self, event, statement):
        if isinstance(statement.get('request'), BEvent):
            if isinstance(statement.get('waitFor'), BEvent):
                return statement.get('request') == event or statement.get('waitFor') == event
            else:
                return statement.get('request') == event or statement.get('waitFor', EmptyEventSet()).contains(event)
        else:
            if isinstance(statement.get('waitFor'), BEvent):
                return statement.get('request', EmptyEventSet()).contains(event) or statement.get('waitFor') == event
            else:
                return statement.get('request', EmptyEventSet()).contains(event) or statement.get('waitFor', EmptyEventSet()).contains(event)

    def selectable_events(self, statements):
        possible_events = set()
        for statement in statements:
            if 'request' in statement:  # should be eligible for sets
                possible_events.add(statement['request'])
        for statement in statements:
            if 'block' in statement:
                possible_events.discard(statement['block'])
        return possible_events

    def select(self, statements):
        selectable_events = self.selectable_events(statements)
        if selectable_events:
            return random.choice(tuple(selectable_events))
        else:
            return None

