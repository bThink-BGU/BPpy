import unittest
from bppy import *
from bppy.utils.dfs import DFSBThread


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