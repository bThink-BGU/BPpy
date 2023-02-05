from bppy.model.event_selection.event_selection_strategy import EventSelectionStrategy
from abc import abstractmethod

class SolverBasedEventSelectionStrategy(EventSelectionStrategy):
    @abstractmethod
    def select(self, statements, external_events_queue=[]):
        pass

    @abstractmethod
    def is_satisfied(self, event, statement):
        pass
