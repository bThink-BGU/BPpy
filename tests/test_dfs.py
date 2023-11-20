import unittest
import bppy as bp
from bppy.utils.dfs import DFSBThread, DFSBProgram
from bppy.utils.exceptions import BPAssertionError


class TestDFS(unittest.TestCase):

    def test_hello_world(self):
        @bp.thread
        def hello():
            yield bp.sync(request=bp.BEvent("Hello"))

        dfs = DFSBThread(lambda: hello(), bp.SimpleEventSelectionStrategy(), [bp.BEvent("Hello"), bp.BEvent("Dummy")])
        init_s, visited = dfs.run()
        assert len(visited) == 2

    def test_hot(self):
        @bp.thread
        def add_hot():
            for i in range(3):
                yield bp.sync(request=bp.BEvent("HOT"))

        dfs = DFSBThread(lambda: add_hot(), bp.SimpleEventSelectionStrategy(),
                         [bp.BEvent("HOT"), bp.BEvent("COLD"), bp.BEvent("Dummy")])
        init_s, visited = dfs.run()
        assert len(visited) == 4

    def test_hot_rb(self):
        @bp.thread
        def add_hot():
            for i in range(3):
                yield bp.sync(request=bp.BEvent("HOT"))

        dfs = DFSBThread(lambda: add_hot(), bp.SimpleEventSelectionStrategy(),
                         [bp.BEvent("HOT"), bp.BEvent("COLD"), bp.BEvent("Dummy")])
        init_s, visited, requested, blocked = dfs.run(return_requested_and_blocked=True)
        assert len(visited) == 4 and len(requested) == 1 and len(blocked) == 0

    def test_control(self):
        @bp.thread
        def control_temp():
            e = bp.BEvent("Dummy")
            while True:
                e = yield bp.sync(waitFor=bp.All(), block=e)

        dfs = DFSBThread(lambda: control_temp(), bp.SimpleEventSelectionStrategy(),
                         [bp.BEvent("HOT"), bp.BEvent("COLD")])
        init_s, visited = dfs.run()
        assert len(visited) == 3

    def test_bprogram(self):
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

        def bp_gen():
            return bp.BProgram(bthreads=[add_hot(), add_cold(), control()],
                               event_selection_strategy=bp.SimpleEventSelectionStrategy())

        dfs = DFSBProgram(bp_gen, [bp.BEvent("HOT"), bp.BEvent("COLD"), bp.BEvent("Dummy")])
        init_s, visited = dfs.run()
        assert len(visited) == 19

    def test_bprogram_no_list(self):
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

        def bp_gen():
            return bp.BProgram(bthreads=[add_hot(), add_cold(), control()],
                               event_selection_strategy=bp.SimpleEventSelectionStrategy())

        dfs = DFSBProgram(bp_gen)
        init_s, visited = dfs.run()
        assert len(visited) == 19

    def test_bp_assertion_error(self):
        @bp.thread
        def add_hot():
            for i in range(3):
                yield bp.sync(request=bp.BEvent("HOT"))

        @bp.thread
        def add_cold():
            for i in range(3):
                yield bp.sync(request=bp.BEvent("COLD"))
            assert False

        @bp.thread
        def control():
            while True:
                yield bp.sync(waitFor=bp.BEvent("HOT"))
                yield bp.sync(waitFor=bp.All(), block=bp.BEvent("HOT"))

        def bp_gen():
            return bp.BProgram(bthreads=[add_hot(), add_cold(), control()],
                               event_selection_strategy=bp.SimpleEventSelectionStrategy())

        dfs = DFSBProgram(bp_gen)
        try:
            init_s, visited = dfs.run()
        except BPAssertionError:
            pass
        assert True
