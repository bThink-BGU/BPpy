from abc import ABC, abstractmethod


class BProgramRunnerListener(ABC):

    @abstractmethod
    def starting(self, b_program):
        pass

    @abstractmethod
    def started(self, b_program):
        pass

    @abstractmethod
    def super_step_done(self, b_program):
        pass

    @abstractmethod
    def ended(self, b_program):
        pass

    @abstractmethod
    def assertion_failed(self, b_program):
        pass

    @abstractmethod
    def b_thread_added(self, b_program):
        pass

    @abstractmethod
    def b_thread_removed(self, b_program):
        pass

    @abstractmethod
    def b_thread_done(self, b_program):
        pass

    @abstractmethod
    def event_selected(self, b_program, event):
        pass

    @abstractmethod
    def halted(self, b_program):
        pass

