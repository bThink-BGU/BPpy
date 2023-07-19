from bppy.model.event_selection.event_selection_strategy import EventSelectionStrategy
from abc import abstractmethod

class SolverBasedEventSelectionStrategy(EventSelectionStrategy):
    """
    A base class used to represent a Solver based Event Selection Strategy. This is an abstract class
    that requires the implementation of `select` and `is_satisfied` methods.
    """
    @abstractmethod
    def select(self, statements, external_events_queue=[]):
        """
        Abstract method to select and return the bprogram's next event. For more information,
        see :class:`SMTEventSelectionStrategy
        <bppy.model.event_selection.smt_event_selection_strategy.SMTEventSelectionStrategy>`.
        """
        pass

    @abstractmethod
    def is_satisfied(self, event, statement):
        """
        Abstract method to check whether a given event satisfies the given sync statement, and the bthread should
        advance. For more information, see :class:`SMTEventSelectionStrategy
        <bppy.model.event_selection.smt_event_selection_strategy.SMTEventSelectionStrategy>`.
        """
        pass

