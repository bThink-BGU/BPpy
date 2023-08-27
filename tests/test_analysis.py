import unittest
from bppy import *
from bppy.analysis.dfs_bprogram_verifier import DFSBProgramVerifier
from bppy.analysis.symbolic_bprogram_verifier import SymbolicBProgramVerifier


class TestAnalysis(unittest.TestCase):

    def test_dfs_failed(self):
        @b_thread
        def add_hot():
            for i in range(3):
                yield {request: BEvent("HOT")}

        @b_thread
        def add_cold():
            for i in range(3):
                yield {request: BEvent("COLD")}

        @b_thread
        def control():
            while True:
                yield {waitFor: BEvent("HOT")}
                yield {waitFor: All(), block: BEvent("HOT")}

        @b_thread
        def check():
            yield {waitFor: BEvent("HOT")}
            yield {waitFor: BEvent("HOT")}
            yield {waitFor: BEvent("HOT")}
            assert False

        def bp_gen():
            return BProgram(bthreads=[add_hot(), add_cold(), control(), check()],
                            event_selection_strategy=SimpleEventSelectionStrategy())

        ver = DFSBProgramVerifier(bp_gen)
        ok, counter_example = ver.verify()
        assert not ok

    def test_dfs_passed(self):
        @b_thread
        def add_hot():
            for i in range(3):
                yield {request: BEvent("HOT")}

        @b_thread
        def add_cold():
            for i in range(3):
                yield {request: BEvent("COLD")}

        @b_thread
        def control():
            while True:
                yield {waitFor: BEvent("HOT")}
                yield {waitFor: All(), block: BEvent("HOT")}

        @b_thread
        def check():
            yield {waitFor: BEvent("HOT")}
            yield {waitFor: BEvent("HOT")}
            yield {waitFor: BEvent("HOT")}
            yield {waitFor: BEvent("HOT")}
            assert False

        def bp_gen():
            return BProgram(bthreads=[add_hot(), add_cold(), control(), check()],
                            event_selection_strategy=SimpleEventSelectionStrategy())

        ver = DFSBProgramVerifier(bp_gen)
        ok, counter_example = ver.verify()
        assert ok

    def test_symbolic_pass(self):

        @b_thread
        def add_hot():
            for i in range(3):
                yield {request: BEvent("HOT")}
            yield {request: BEvent("FINISH"), block: {BEvent("COLD")}}

        @b_thread
        def add_cold():
            for i in range(3):
                yield {request: BEvent("COLD")}

        @b_thread
        def control():
            while True:
                yield {waitFor: BEvent("HOT"), block: EventSet(lambda e: e.name == "COLD")}
                yield {waitFor: All(), block: BEvent("HOT")}

        def bp_gen():
            return BProgram(bthreads=[add_hot(), add_cold(), control()])

        verifier = SymbolicBProgramVerifier(bp_gen, [BEvent("HOT"), BEvent("COLD"), BEvent("FINISH")])
        result, explanation_str = verifier.verify(spec="F event = FINISH", type="BDD", bound=1000,
                                                  find_counterexample=True, print_info=False)

        assert result

    def test_symbolic_fail(self):

        @b_thread
        def add_hot():
            for i in range(3):
                yield {request: BEvent("HOT")}
            yield {request: BEvent("FINISH"), block: {BEvent("COLD")}}

        @b_thread
        def add_cold():
            for i in range(3):
                yield {request: BEvent("COLD")}

        @b_thread
        def control():
            while True:
                yield {waitFor: BEvent("HOT")}
                yield {waitFor: All(), block: BEvent("HOT")}

        def bp_gen():
            return BProgram(bthreads=[add_hot(), add_cold(), control()])

        verifier = SymbolicBProgramVerifier(bp_gen, [BEvent("HOT"), BEvent("COLD"), BEvent("FINISH")])
        result, explanation_str = verifier.verify(spec="F event = FINISH", type="BMC", bound=100,
                                                  find_counterexample=True, print_info=False)

        assert not result and explanation_str is not None

