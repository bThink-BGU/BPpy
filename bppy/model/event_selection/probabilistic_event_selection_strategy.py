from bppy.model.event_selection.event_selection_strategy import EventSelectionStrategy
from bppy.model.b_event import BEvent
from bppy.model.event_set import EmptyEventSet
import random
from collections.abc import Iterable


class ProbabilisticEventSelectionStrategy(EventSelectionStrategy):
    """
    A simple :class:`EventSelectionStrategy
    <bppy.model.event_selection.event_selection_strategy.EventSelectionStrategy>`, which uniformly selects an event
    that is requested and not blocked. It advances all bthreads that requested or waited for the selected event.
    """
    def is_satisfied(self, event, statement):
        """
        Checks whether a bthread should advance based on the selected event and its current sync statement.
        Specifically, It checks whether the statement requests or waits for the selected event.

        Parameters
        ----------
        event : :class:`BEvent <bppy.model.b_event.BEvent>`
            The selected event to be checked against the statement.
        statement : dict
            The bthread's sync statement to check the selected event against.

        Returns
        -------
        bool
            True if the statement requests or waits for the selected event, False otherwise.
        """
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
        """
        Returns a set of possible events that can be selected from a list of bthread statements. Specifically,
        the method extracts requested non-blocked events from the provided bthreads statements.

        Parameters
        ----------
        statements : list
            A list of bthreads sync statements from which to extract selectable events.

        Returns
        -------
        set
            A set of events that can be selected.
        events_weight: dict
            The probability of each event to be selected given the statement.
        """
        possible_events = set()
        events_weight = {}
        for statement in statements:
            if 'request' in statement:  # should be eligible for sets
                req_count = (len(statement['request']) if isinstance(statement['request'], Iterable) else 1)
                statement_weight = []
                if 'weight' in statement:
                    if len(statement['weight']) != req_count:
                       raise ValueError("weights length should match the number of requested events")
                    statement_weight = statement['weight']
                else:
                    statement_weight = [1./req_count] * req_count
                if isinstance(statement['request'], Iterable):
                    possible_events.update(statement['request'])
                    for i, e in enumerate(statement['request']):
                        events_weight[e] = statement_weight[i]
                elif isinstance(statement['request'], BEvent):
                    possible_events.add(statement['request'])
                    events_weight[statement['request']] = 1
                else:
                    raise TypeError("request parameter should be BEvent or iterable")
        for statement in statements:
            if 'block' in statement:
                if isinstance(statement.get('block'), BEvent):
                    possible_events.discard(statement.get('block'))
                else:
                    possible_events = {x for x in possible_events if x not in statement.get('block')}
        return possible_events, events_weight

    def select(self, statements, external_events_queue=[]):
        """
        Selects the next event from the given statements and external events queue.

        This method selects the next event uniformly at random from the set of selectable events If no events can be
        selected from the statements, an event from the external events queue will be selected (or `None` is returned
        if the queue is empty).

        Parameters
        ----------
        statements : list
            A list of bthreads sync statements from which an event will be selected.
        external_events_queue : list, optional
            A list of external events that may be selected.

        Returns
        -------
        :class:`BEvent <bppy.model.b_event.BEvent>` or `None`
            The selected event, or `None` if no event can be selected.
        """
        selectable_events, events_weight = self.selectable_events(statements)
        selectable_weights = [events_weight[e] for e in selectable_events]
        print([w for w in zip(selectable_events, selectable_weights)])
        if selectable_events:
            return random.choices(tuple(selectable_events), selectable_weights)[0]
        else:
            if len(external_events_queue) > 0:
                return external_events_queue.pop(0)
            else:
                return None

