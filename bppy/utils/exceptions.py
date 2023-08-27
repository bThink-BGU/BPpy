class BPAssertionError(AssertionError):
    def __init__(self, msg, trace):
        self.trace = trace
        super().__init__(msg)
