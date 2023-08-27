from bppy.utils.dfs import DFSBProgram
from bppy.utils.exceptions import BPAssertionError


class DFSBProgramVerifier:
    """
    A class to verify a behavioral program using Depth First Search (DFS). Currently, this class verifies only
    properties which can be defined using assertions in b-threads. For additional properties, or programs with large
    state space, use :class:`SymbolicBProgramVerifier
    <bppy.analysis.symbolic_bprogram_verifier.SymbolicBProgramVerifier>`.

    Attributes:
    -----------
    bprogram_generator : function
        A function that generates a new instance of the BProgram.
    max_trace_length : int
        Maximum length of the trace before terminating the search.
    """
    def __init__(self, bprogram_generator, max_trace_length=1000):
        """
        Initialize a DFSBProgramVerifier.

        Parameters:
        -----------
        bprogram_generator : function
            A function that generates a new instance of the BProgram.
        max_trace_length : int, optional
            Maximum length of the trace before terminating the search. Defaults to 1000.
        """
        self.bprogram_generator = bprogram_generator
        self.max_trace_length = max_trace_length

    def verify(self):
        """
        Execute a DFS on the behavioral program to check for assertion errors.

        Returns:
        --------
        bool:
            True if no assertion error is encountered, otherwise False.
        Optional[tuple]:
            Trace leading up to the assertion error, if one is encountered. Otherwise, None.
        """
        dfs = DFSBProgram(self.bprogram_generator, max_trace_length=self.max_trace_length)
        try:
            _, _ = dfs.run()
            return True, None
        except BPAssertionError as e:
            return False, e.trace
