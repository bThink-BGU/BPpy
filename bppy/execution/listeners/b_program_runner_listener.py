from abc import ABC, abstractmethod


class BProgramRunnerListener(ABC):
    """
    Abstract Base Class representing a listener for :class:`BProgram <bppy.model.bprogram.BProgram>` execution events.
    """
    @abstractmethod
    def starting(self, b_program):
        """
        Abstract method to handle the start of the execution of a :class:`BProgram <bppy.model.bprogram.BProgram>`.
        """
        pass

    @abstractmethod
    def started(self, b_program):
        """
        Abstract method to handle the start of the execution of a :class:`BProgram <bppy.model.bprogram.BProgram>`.
        """
        pass

    @abstractmethod
    def super_step_done(self, b_program):
        """
        Abstract method to handle the completion of a super-step of a :class:`BProgram <bppy.model.bprogram.BProgram>`.
        """
        pass

    @abstractmethod
    def ended(self, b_program):
        """
        Abstract method to handle the end of the execution of a :class:`BProgram <bppy.model.bprogram.BProgram>`.
        """
        pass

    @abstractmethod
    def assertion_failed(self, b_program):
        """
        Abstract method to handle assertion failures in the execution of a :class:`BProgram <bppy.model.bprogram.BProgram>`.
        """
        pass

    @abstractmethod
    def b_thread_added(self, b_program):
        """
        Abstract method to handle the addition of a bthread in the :class:`BProgram <bppy.model.bprogram.BProgram>`.
        """
        pass

    @abstractmethod
    def b_thread_removed(self, b_program):
        """
        Abstract method to handle the removal of a bthread in the :class:`BProgram <bppy.model.bprogram.BProgram>`.
        """
        pass

    @abstractmethod
    def b_thread_done(self, b_program):
        """
        Abstract method to handle the termination of a bthread in the execution of a :class:`BProgram <bppy.model.bprogram.BProgram>`.
        """
        pass

    @abstractmethod
    def event_selected(self, b_program, event):
        """
        Abstract method to handle the selection of event during the execution of a :class:`BProgram <bppy.model.bprogram.BProgram>`.
        """
        pass

    @abstractmethod
    def halted(self, b_program):
        """
        Abstract method to handle the halting of the execution of a :class:`BProgram <bppy.model.bprogram.BProgram>`.
        """
        pass

