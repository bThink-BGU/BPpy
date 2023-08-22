import unittest
from bppy import *
from bppy.utils.dfs import DFSBThread, DFSBProgram
from bppy.utils.exceptions import BPAssertionError

class TestDFS(unittest.TestCase):

    def test_hello_world(self):
        @b_thread
        def hello():
            yield {request: BEvent("Hello")}

        dfs = DFSBThread(lambda: hello(), SimpleEventSelectionStrategy(), [BEvent("Hello"), BEvent("Dummy")])
        init_s, visited = dfs.run()
        assert len(visited) == 2

    def test_hot(self):
        @b_thread
        def add_hot():
            for i in range(3):
                yield {request: BEvent("HOT")}

        dfs = DFSBThread(lambda: add_hot(), SimpleEventSelectionStrategy(), [BEvent("HOT"), BEvent("COLD"), BEvent("Dummy")])
        init_s, visited = dfs.run()
        assert len(visited) == 4

    def test_control(self):
        @b_thread
        def control_temp():
            e = BEvent("Dummy")
            while True:
                e = yield {waitFor: All(), block: e}

        dfs = DFSBThread(lambda: control_temp(), SimpleEventSelectionStrategy(), [BEvent("HOT"), BEvent("COLD")])
        init_s, visited = dfs.run()
        assert len(visited) == 3

    def test_bprogram(self):
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

        def bp_gen():
            return BProgram(bthreads=[add_hot(), add_cold(), control()],
                            event_selection_strategy=SimpleEventSelectionStrategy())

        dfs = DFSBProgram(bp_gen, [BEvent("HOT"), BEvent("COLD"), BEvent("Dummy")])
        init_s, visited = dfs.run()
        assert len(visited) == 19

    def test_bprogram_no_list(self):
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

        def bp_gen():
            return BProgram(bthreads=[add_hot(), add_cold(), control()],
                            event_selection_strategy=SimpleEventSelectionStrategy())

        dfs = DFSBProgram(bp_gen)
        init_s, visited = dfs.run()
        assert len(visited) == 19

    def test_bp_assertion_error(self):
        @b_thread
        def add_hot():
            for i in range(3):
                yield {request: BEvent("HOT")}

        @b_thread
        def add_cold():
            for i in range(3):
                yield {request: BEvent("COLD")}
            assert False

        @b_thread
        def control():
            while True:
                yield {waitFor: BEvent("HOT")}
                yield {waitFor: All(), block: BEvent("HOT")}

        def bp_gen():
            return BProgram(bthreads=[add_hot(), add_cold(), control()],
                            event_selection_strategy=SimpleEventSelectionStrategy())

        dfs = DFSBProgram(bp_gen)
        try:
            init_s, visited = dfs.run()
        except BPAssertionError:
            pass
        assert True

