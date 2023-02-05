from abc import ABC, abstractmethod


class EventSelectionStrategy(ABC):

    @abstractmethod
    def select(self, statements, external_events_queue=[]):
        pass

    @abstractmethod
    def is_satisfied(self, event, statement):
        pass
