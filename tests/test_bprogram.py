import unittest
import bppy as bp


class TestBProgram(unittest.TestCase):

    def test_advance_bthreads(self):
        @bp.thread
        def hello():  # requests "Hello" once
            yield bp.sync(request=bp.BEvent("Hello"))

        @bp.thread
        def world():  # requests "World" once
            yield bp.sync(request=bp.BEvent("World"))

        b_program = bp.BProgram(bthreads=[hello(), world()],
                             event_selection_strategy=bp.SimpleEventSelectionStrategy())

        b_program.setup()
        b_program.advance_bthreads(b_program.tickets, bp.BEvent("Hello"))
        b_program.advance_bthreads(b_program.tickets, bp.BEvent("World"))
        assert all([len(x) == 0 for x in b_program.tickets]) and len(b_program.tickets) == 2
