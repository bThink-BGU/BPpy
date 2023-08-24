from bppy.utils.dfs import DFSBProgram
from bppy.utils.exceptions import BPAssertionError


class DFSBProgramVerifier:
    def __init__(self, bprogram_generator, max_trace_length=1000):
        self.bprogram_generator = bprogram_generator
        self.max_trace_length = max_trace_length

    def verify(self):
        dfs = DFSBProgram(self.bprogram_generator, max_trace_length=self.max_trace_length)
        try:
            _, _ = dfs.run()
            return True, None
        except BPAssertionError as e:
            return False, e.trace
