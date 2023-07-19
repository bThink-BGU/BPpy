from bppy.model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy
from collections.abc import Iterable
from bppy.model.b_event import BEvent


class PriorityBasedEventSelectionStrategy(SimpleEventSelectionStrategy):
    """
    Priority-based extension for :class:`SimpleEventSelectionStrategy
    <bppy.model.event_selection.event_selection_strategy.SimpleEventSelectionStrategy>`, selecting the requested
    non-blocked event with the highest priority. If no priority is specified for an event, the `default_priority`
    attribute is used.

    Attributes
    ----------
    default_priority : int
        The default priority value to use if no priority is specified for an event.
    """
    def __init__(self, default_priority=0):
        """
        Constructs a new PriorityBasedEventSelectionStrategy with a given default priority.

        Parameters
        ----------
        default_priority : int, optional
            The default priority to be used when no specific priority is given for an event.
        """
        self.default_priority = default_priority

    def selectable_events(self, statements):
        """
        Returns a set of possible events that can be selected from a list of bthread statements. Specifically,
        the method extracts requested non-blocked events, with the maximal priority value, from the provided bthreads statements.

        Parameters
        ----------
        statements : list
            A list of bthread statements from which to extract possible events.

        Returns
        -------
        set
            A set of possible events that can be selected.
        """
        possible_events = set()
        for statement in statements:
            if 'request' in statement:  # should be eligible for sets
                p = statement.get('priority', self.default_priority)
                if isinstance(statement['request'], Iterable):
                    possible_events.update([(x, p) for x in statement['request']])
                elif isinstance(statement['request'], BEvent):
                    possible_events.add((statement['request'], p))
                else:
                    raise TypeError("request parameter should be BEvent or iterable")
        for statement in statements:
            if 'block' in statement:
                if isinstance(statement.get('block'), BEvent):
                    possible_events = {(x, p) for x, p in possible_events if x != statement.get('block')}
                else:
                    possible_events = {(x, p) for x, p in possible_events if x not in statement.get('block')}
        if len(possible_events) == 0:
            return possible_events
        max_priority = max([p for _, p in possible_events])
        return {x for x, p in possible_events if p == max_priority}
