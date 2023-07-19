from abc import ABC, abstractmethod


class EventSelectionStrategy(ABC):
    """
    A base class used to represent an Event Selection Strategy. This is an abstract class
    that requires the implementation of `select` and `is_satisfied` methods.
    """
    @abstractmethod
    def select(self, statements, external_events_queue=[]):
        """
        Abstract method to select and return the bprogram's next event.

        This method needs to be implemented in child classes. It takes a list of statements
        and an external events queue, and should return the next event to be selected based
        on the strategy being implemented.

        Parameters
        ----------
        statements : list
            A list of bthread statements from which an event will be selected.
        external_events_queue : list, optional
            A list of external events that may be selected.

        Returns
        -------
        Abstract
            Returns the next event to be selected based on the strategy being implemented,
            or `None` if no event can be selected
        """
        pass

    @abstractmethod
    def is_satisfied(self, event, statement):
        """
        Abstract method to check whether a given event satisfies the given sync statement, and the bthread should
        advance.

        This method needs to be implemented in child classes. It takes an event and a
        statement, and should return a boolean indicating whether the event satisfies
        the statement and the bthread should advance according to the strategy being implemented.

        Parameters
        ----------
        event : :class:`BEvent <bppy.model.b_event.BEvent>`
            The event to be checked against the statement.
        statement : dict
            The statement to check the event against.

        Returns
        -------
        Abstract
            Returns a boolean indicating whether the event satisfies the statement
            and the bthread should advance according to the strategy being implemented.
        """
        pass
