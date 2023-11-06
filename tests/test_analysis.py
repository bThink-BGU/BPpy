import unittest
import bppy as bp
from bppy.analysis.dfs_bprogram_verifier import DFSBProgramVerifier
from bppy.analysis.symbolic_bprogram_verifier import SymbolicBProgramVerifier


class TestAnalysis(unittest.TestCase):

    def test_dfs_failed(self):
        @bp.thread
        def add_hot():
            for i in range(3):
                yield bp.sync(request=bp.BEvent("HOT"))

        @bp.thread
        def add_cold():
            for i in range(3):
                yield bp.sync(request=bp.BEvent("COLD"))

        @bp.thread
        def control():
            while True:
                yield bp.sync(waitFor=bp.BEvent("HOT"))
                yield bp.sync(waitFor=bp.All(), block=bp.BEvent("HOT"))

        @bp.thread
        def check():
            yield bp.sync(waitFor=bp.BEvent("HOT"))
            yield bp.sync(waitFor=bp.BEvent("HOT"))
            yield bp.sync(waitFor=bp.BEvent("HOT"))
            assert False

        def bp_gen():
            return bp.BProgram(bthreads=[add_hot(), add_cold(), control(), check()],
                               event_selection_strategy=bp.SimpleEventSelectionStrategy())

        ver = DFSBProgramVerifier(bp_gen)
        ok, counter_example = ver.verify()
        assert not ok

    def test_dfs_passed(self):
        @bp.thread
        def add_hot():
            for i in range(3):
                yield bp.sync(request=bp.BEvent("HOT"))

        @bp.thread
        def add_cold():
            for i in range(3):
                yield bp.sync(request=bp.BEvent("COLD"))

        @bp.thread
        def control():
            while True:
                yield bp.sync(waitFor=bp.BEvent("HOT"))
                yield bp.sync(waitFor=bp.All(), block=bp.BEvent("HOT"))

        @bp.thread
        def check():
            yield bp.sync(waitFor=bp.BEvent("HOT"))
            yield bp.sync(waitFor=bp.BEvent("HOT"))
            yield bp.sync(waitFor=bp.BEvent("HOT"))
            yield bp.sync(waitFor=bp.BEvent("HOT"))
            assert False

        def bp_gen():
            return bp.BProgram(bthreads=[add_hot(), add_cold(), control(), check()],
                               event_selection_strategy=bp.SimpleEventSelectionStrategy())

        ver = DFSBProgramVerifier(bp_gen)
        ok, counter_example = ver.verify()
        assert ok

    def test_symbolic_pass(self):

        @bp.thread
        def add_hot():
            for i in range(3):
                yield bp.sync(request=bp.BEvent("HOT"))
            yield bp.sync(request=bp.BEvent("FINISH"), block={bp.BEvent("COLD")})

        @bp.thread
        def add_cold():
            for i in range(3):
                yield bp.sync(request=bp.BEvent("COLD"))

        @bp.thread
        def control():
            while True:
                yield bp.sync(waitFor=bp.BEvent("HOT"), block=bp.EventSet(lambda e: e.name == "COLD"))
                yield bp.sync(waitFor=bp.All(), block=bp.BEvent("HOT"))

        def bp_gen():
            return bp.BProgram(bthreads=[add_hot(), add_cold(), control()])

        verifier = SymbolicBProgramVerifier(bp_gen, [bp.BEvent("HOT"), bp.BEvent("COLD"), bp.BEvent("FINISH")])
        result, explanation_str = verifier.verify(spec="F event = FINISH", type="BDD", bound=1000,
                                                  find_counterexample=True, print_info=False)

        assert result

    def test_symbolic_fail(self):

        @bp.thread
        def add_hot():
            for i in range(3):
                yield bp.sync(request=bp.BEvent("HOT"))
            yield bp.sync(request=bp.BEvent("FINISH"), block=[bp.BEvent("COLD")])

        @bp.thread
        def add_cold():
            for i in range(3):
                yield bp.sync(request=bp.BEvent("COLD"))

        @bp.thread
        def control():
            while True:
                yield bp.sync(waitFor=bp.BEvent("HOT"))
                yield bp.sync(waitFor=bp.All(), block=bp.BEvent("HOT"))

        def bp_gen():
            return bp.BProgram(bthreads=[add_hot(), add_cold(), control()])

        verifier = SymbolicBProgramVerifier(bp_gen, [bp.BEvent("HOT"), bp.BEvent("COLD"), bp.BEvent("FINISH")])
        result, explanation_str = verifier.verify(spec="F event = FINISH", type="BMC", bound=100,
                                                  find_counterexample=True, print_info=False)

        assert not result and explanation_str is not None
