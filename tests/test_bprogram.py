import unittest
from bppy import *


class TestBProgram(unittest.TestCase):

    def test_advance_bthreads(self):
        @b_thread
        def hello():
            yield {request: BEvent("Hello")}

        @b_thread
        def world():
            yield {request: BEvent("World")}

        b_program = BProgram(bthreads=[hello(), world()],
                             event_selection_strategy=SimpleEventSelectionStrategy())

        b_program.setup()
        b_program.advance_bthreads(b_program.tickets, BEvent("Hello"))
        b_program.advance_bthreads(b_program.tickets, BEvent("World"))
        assert all([len(x) == 0 for x in b_program.tickets]) and len(b_program.tickets) == 2
